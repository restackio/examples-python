import asyncio
import os

import aiohttp
from dotenv import load_dotenv
from pipecat.audio.vad.silero import SileroVADAnalyzer
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineParams, PipelineTask
from pipecat.processors.aggregators.openai_llm_context import (
    OpenAILLMContext,
)
from pipecat.services.cartesia import CartesiaTTSService
from pipecat.services.deepgram import DeepgramSTTService
from pipecat.services.openai import OpenAILLMService
from pipecat.transports.services.daily import (
    DailyParams,
    DailyTransport,
)
from pipecat.transports.services.helpers.daily_rest import (
    DailyRESTHelper,
    DailyRoomParams,
    DailyRoomProperties,
)
from pydantic import BaseModel
from restack_ai.function import (
    NonRetryableError,
    function,
    function_info,
    log,
)

from src.functions.heygen_client import (
    HeyGenClient,
    NewSessionRequest,
)
from src.functions.heygen_video_service import HeyGenVideoService

load_dotenv(override=True)


class PipecatPipelineHeygenInput(BaseModel):
    agent_name: str
    agent_id: str
    agent_run_id: str


def get_agent_backend_host(engine_api_address: str) -> str:
    if not engine_api_address:
        return "http://localhost:9233"
    if not engine_api_address.startswith("https://"):
        return "https://" + engine_api_address
    return engine_api_address


async def create_daily_room(
    session: aiohttp.ClientSession,
    room_id: str,
) -> DailyRoomParams:
    daily_rest_helper = DailyRESTHelper(
        daily_api_key=os.getenv("DAILYCO_API_KEY"),
        daily_api_url="https://api.daily.co/v1",
        aiohttp_session=session,
    )
    return await daily_rest_helper.create_room(
        params=DailyRoomParams(
            name=room_id,
            properties=DailyRoomProperties(
                start_video_off=True,
                start_audio_off=False,
                max_participants=2,
                enable_prejoin_ui=False,
            ),
        ),
    )


async def get_daily_token(
    daily_rest_helper: DailyRESTHelper,
    room_url: str,
    expiry_time: float,
) -> str:
    return await daily_rest_helper.get_token(
        room_url,
        expiry_time,
    )


@function.defn(name="pipecat_pipeline_heygen")
async def pipecat_pipeline_heygen(
    function_input: PipecatPipelineHeygenInput,
) -> str:
    try:
        async with aiohttp.ClientSession() as session:
            room_id = function_info().workflow_run_id

            engine_api_address = os.environ.get(
                "RESTACK_ENGINE_API_ADDRESS",
            )
            agent_backend_host = get_agent_backend_host(
                engine_api_address,
            )

            log.info(
                "Using RESTACK_ENGINE_API_ADDRESS",
                agent_backend_host=agent_backend_host,
            )

            agent_url = f"{agent_backend_host}/stream/agents/{function_input.agent_name}/{function_input.agent_id}/{function_input.agent_run_id}"
            log.info("Agent URL", agent_url=agent_url)

            room = await create_daily_room(session, room_id)

            expiry_time: float = 60 * 60

            daily_rest_helper = DailyRESTHelper(
                daily_api_key=os.getenv("DAILYCO_API_KEY"),
                daily_api_url="https://api.daily.co/v1",
                aiohttp_session=session,
            )

            daily_token = await get_daily_token(
                daily_rest_helper,
                room.url,
                expiry_time,
            )

            transport = DailyTransport(
                room_url=room.url,
                token=daily_token,
                bot_name="HeyGen",
                params=DailyParams(
                    audio_out_enabled=True,
                    camera_out_enabled=True,
                    camera_out_width=854,
                    camera_out_height=480,
                    vad_enabled=True,
                    vad_analyzer=SileroVADAnalyzer(),
                    transcription_enabled=True,
                ),
            )

            stt = DeepgramSTTService(
                api_key=os.getenv("DEEPGRAM_API_KEY"),
            )

            tts = CartesiaTTSService(
                api_key=os.getenv("CARTESIA_API_KEY"),
                voice_id=os.getenv("CARTESIA_VOICE_ID"),
                sample_rate=24000,
            )

            llm = OpenAILLMService(
                api_key="pipecat-pipeline",
                base_url=agent_url,
            )

            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are Philippe Brule, CTO and co-founder of restack : the entreprise-grade backend framework to help develoeprs build reliable and accurate AI agents. You live in San Francisco, California."
                    ),
                },
            ]

            context = OpenAILLMContext(messages)
            context_aggregator = llm.create_context_aggregator(
                context,
            )

            heygen_client = HeyGenClient(
                api_key=os.getenv("HEYGEN_API_KEY"),
                session=session,
            )

            session_response = await heygen_client.new_session(
                NewSessionRequest(
                    avatarName="Bryan_IT_Sitting_public",
                    version="v2",
                ),
            )

            await heygen_client.start_session(
                session_response.session_id,
            )

            heygen_video_service = HeyGenVideoService(
                session_id=session_response.session_id,
                session_token=session_response.access_token,
                session=session,
                realtime_endpoint=session_response.realtime_endpoint,
                livekit_room_url=session_response.url,
            )

            pipeline = Pipeline(
                [
                    transport.input(),  # Transport user input
                    stt,  # STT
                    context_aggregator.user(),  # User responses
                    llm,  # LLM
                    tts,  # TTS
                    heygen_video_service,  # HeyGen output layer replacing Tavus
                    transport.output(),  # Transport bot output
                    context_aggregator.assistant(),  # Assistant spoken responses
                ],
            )

            task = PipelineTask(
                pipeline,
                params=PipelineParams(
                    allow_interruptions=True,
                    enable_metrics=True,
                    enable_usage_metrics=True,
                    report_only_initial_ttfb=True,
                ),
            )

            @transport.event_handler(
                "on_first_participant_joined",
            )
            async def on_first_participant_joined(
                transport: DailyTransport,
                participant: dict,
            ) -> None:
                await transport.capture_participant_transcription(
                    participant["id"],
                )
                messages.append(
                    {
                        "role": "system",
                        "content": "Please introduce yourself to the user. Keep it short and concise.",
                    },
                )
                await task.queue_frames(
                    [
                        context_aggregator.user().get_context_frame(),
                    ],
                )

            @transport.event_handler("on_participant_left")
            async def on_participant_left() -> None:
                await task.cancel()

            runner = PipelineRunner()

            async def run_pipeline() -> None:
                try:
                    log.info("Running pipeline")
                    await runner.run(task)
                except Exception as e:
                    error_message = "Pipeline runner encountered an error, cancelling pipeline"
                    log.error(error_message, error=e)
                    # Cancel the pipeline task if an error occurs within the pipeline runner.
                    await task.cancel()
                    raise NonRetryableError(error_message) from e

            # Launch the pipeline runner as a background task so it doesn't block the return.
            pipeline_task = asyncio.create_task(run_pipeline())
            pipeline_task.add_done_callback(
                lambda t: t.exception()
                if t.exception() is not None
                else None,
            )

            room_url = room.url

            log.info(
                "Pipecat HeyGen pipeline started",
                room_url=room_url,
            )

            # Return the room_url immediately.
            return room_url
    except Exception as e:
        error_message = "Pipecat pipeline failed"
        log.error(error_message, error=e)
        raise NonRetryableError(error_message) from e
