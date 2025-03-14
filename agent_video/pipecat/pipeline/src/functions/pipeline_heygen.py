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
    daily_room_url: str
    daily_room_token: str


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
        async with aiohttp.ClientSession() as heygen_session:

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

            transport = DailyTransport(
                room_url=function_input.daily_room_url,
                token=function_input.daily_room_token,
                bot_name="HeyGen",
                params=DailyParams(
                    audio_out_enabled=True,
                    camera_out_enabled=True,
                    camera_out_width=854,
                    camera_out_height=480,
                    vad_enabled=True,
                    vad_analyzer=SileroVADAnalyzer(),
                    transcription_enabled=True,
                    audio_out_sample_rate=HeyGenVideoService.SAMPLE_RATE,
                ),
            )

            stt = DeepgramSTTService(
                api_key=os.getenv("DEEPGRAM_API_KEY"),
            )

            tts = CartesiaTTSService(
                api_key=os.getenv("CARTESIA_API_KEY"),
                voice_id=os.getenv("CARTESIA_VOICE_ID"),
                sample_rate=HeyGenVideoService.SAMPLE_RATE,
                
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
                session=heygen_session,
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
                session=heygen_session,
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
            async def on_participant_left(
                transport: DailyTransport,
                participant: dict,
                reason: str,
            ) -> None:
                log.info(
                    "Participant left",
                    participant=participant,
                    reason=reason,
                )
                await task.cancel()

            runner = PipelineRunner()

            await runner.run(task)

            return 'Pipeline done'
    except Exception as e:
        error_message = "Pipecat pipeline failed"
        log.error(error_message, error=e)
        await task.cancel()
        raise NonRetryableError(error_message) from e
