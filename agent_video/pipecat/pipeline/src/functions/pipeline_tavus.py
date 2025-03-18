import asyncio
import os
from collections.abc import Mapping
from typing import Any

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
from pydantic import BaseModel
from restack_ai.function import NonRetryableError, function, log
from src.functions.tavus_video_service import TavusVideoService
# from pipecat.frames.frames import EndFrame, TTSSpeakFrame

load_dotenv(override=True)


class PipecatPipelineTavusInput(BaseModel):
    agent_name: str
    agent_id: str
    agent_run_id: str
    daily_room_url: str


@function.defn(name="pipecat_pipeline_tavus")
async def pipecat_pipeline_tavus(
    function_input: PipecatPipelineTavusInput,
) -> bool:
    try:
        async with aiohttp.ClientSession() as session:
            engine_api_address = os.environ.get(
                "RESTACK_ENGINE_API_ADDRESS",
            )
            if not engine_api_address:
                agent_backend_host = "http://localhost:9233"
            elif not engine_api_address.startswith("https://"):
                agent_backend_host = (
                    "https://" + engine_api_address
                )
            else:
                agent_backend_host = engine_api_address

            log.info(
                "Using RESTACK_ENGINE_API_ADDRESS",
                agent_backend_host=agent_backend_host,
            )

            agent_url = f"{agent_backend_host}/stream/agents/{function_input.agent_name}/{function_input.agent_id}/{function_input.agent_run_id}"
            log.info("Agent URL", agent_url=agent_url)

            tavus = TavusVideoService(
                api_key=os.getenv("TAVUS_API_KEY"),
                replica_id=os.getenv("TAVUS_REPLICA_ID"),
                session=session,
                conversation_id=function_input.daily_room_url.split("/")[-1],
            )


 
            persona_name = await tavus.get_persona_name()
            
            transport = DailyTransport(
                room_url=function_input.daily_room_url,
                token=None,
                bot_name=persona_name,
                params=DailyParams(
                    audio_out_enabled=True,
                    camera_out_enabled=True,
                    vad_enabled=True,
                    vad_analyzer=SileroVADAnalyzer(),
                    vad_audio_passthrough=True,
                    audio_out_sample_rate=TavusVideoService.SAMPLE_RATE,
                ),
            )

            stt = DeepgramSTTService(
                api_key=os.getenv("DEEPGRAM_API_KEY"),
            )

            tts = CartesiaTTSService(
                api_key=os.getenv("CARTESIA_API_KEY"),
                voice_id=os.getenv("CARTESIA_VOICE_ID"),
                sample_rate=TavusVideoService.SAMPLE_RATE,
            )

            llm = OpenAILLMService(
                api_key="pipecat-pipeline",
                base_url=agent_url,
            )

            messages = [
                {
                    "role": "system",
                    "content": "",
                },
            ]

            context = OpenAILLMContext(messages)
            context_aggregator = llm.create_context_aggregator(
                context,
            )

            pipeline = Pipeline(
                [
                    transport.input(),  # Transport user input
                    stt,  # STT
                    context_aggregator.user(),  # User responses
                    llm,  # LLM
                    tts,  # TTS
                    tavus,  # Tavus output layer
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
                    audio_out_sample_rate=TavusVideoService.SAMPLE_RATE,
                ),
                check_dangling_tasks=True,
            )

            @transport.event_handler("on_participant_joined")
            async def on_participant_joined(
                transport: DailyTransport,
                participant: Mapping[str, Any],
            ) -> None:
                participant_id = participant.get("id")
                if participant_id is None:
                    log.warning(
                        "Participant joined without an 'id', skipping update_subscriptions.",
                    )
                    return

                # Ignore the Tavus replica's microphone
                if (
                    participant.get("info", {}).get(
                        "userName",
                        "",
                    )
                    == persona_name
                ):
                    log.debug(
                        f"Ignoring {participant_id}'s microphone",
                    )
                    await transport.update_subscriptions(
                        participant_settings={
                            str(participant_id): {
                                "media": {
                                    "microphone": "unsubscribed",
                                },
                            },
                        },
                    )
                else:
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

            # @transport.event_handler("on_participant_joined")
            # async def on_participant_joined(transport, participant):
            #     participant_name = participant.get("info", {}).get("userName", "")
            #     await task.queue_frames(
            #         [TTSSpeakFrame(f"Hello there, {participant_name}!"), EndFrame()]
            #     )

            # @transport.event_handler("on_app_message")
            # async def on_app_message(transport, message, sender):
            #     log.info(f"Received {sender} message: {message}")
            #     # author = message.get("author")
            #     # text = message.get("text")
            #     # log.debug(f"Received {sender} message from {author}: {text}")
            #     # await llm.push_frame(TTSSpeakFrame(text))
            #     # await task.queue_frames(
            #     #     [TTSSpeakFrame(text), EndFrame()]
            #     # )

            @transport.event_handler("on_participant_left")
            async def on_participant_left(transport: DailyTransport,
                participant: dict,
                reason: str,) -> None:
                log.info(
                    "Participant left",
                    participant=participant,
                    reason=reason,
                )
                await task.cancel()

            runner = PipelineRunner()

            try:
                await runner.run(task)
            except Exception as e:
                log.error("Pipeline runner error, cancelling pipeline", error=e)
                await task.cancel()
                raise NonRetryableError("Pipeline runner error, cancelling pipeline") from e

            return True
    except Exception as e:
        error_message = "Pipecat pipeline failed"
        log.error(error_message, error=e)
        raise NonRetryableError(error_message) from e
