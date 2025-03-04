#
# Copyright (c) 2024–2025, Daily
#
# SPDX-License-Identifier: BSD 2-Clause License
#
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
from pipecat.processors.aggregators.openai_llm_context import OpenAILLMContext
from pipecat.services.cartesia import CartesiaTTSService
from pipecat.services.deepgram import DeepgramSTTService
from pipecat.services.openai import OpenAILLMService
from pipecat.services.tavus import TavusVideoService
from pipecat.transports.services.daily import DailyParams, DailyTransport
from pydantic import BaseModel
from restack_ai.function import NonRetryableError, function, log

load_dotenv(override=True)


class PipecatPipelineInput(BaseModel):
    agent_name: str
    agent_id: str
    agent_run_id: str


@function.defn(name="pipecat_pipeline")
async def pipecat_pipeline(function_input: PipecatPipelineInput) -> str:
    try:
        async with aiohttp.ClientSession() as session:
            engine_api_address = os.environ.get("RESTACK_ENGINE_API_ADDRESS")
            if not engine_api_address:
                agent_backend_host = "http://localhost:9233"
            elif not engine_api_address.startswith("https://"):
                agent_backend_host = "https://" + engine_api_address
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
            )

            persona_name = await tavus.get_persona_name()
            room_url = await tavus.initialize()

            transport = DailyTransport(
                room_url=room_url,
                token=None,
                bot_name=persona_name,
                params=DailyParams(
                    vad_enabled=True,
                    vad_analyzer=SileroVADAnalyzer(),
                    vad_audio_passthrough=True,
                ),
            )

            stt = DeepgramSTTService(api_key=os.getenv("DEEPGRAM_API_KEY"))

            tts = CartesiaTTSService(
                api_key=os.getenv("CARTESIA_API_KEY"),
                voice_id=os.getenv("CARTESIA_VOICE_ID"),
            )

            llm = OpenAILLMService(api_key="pipecat-pipeline", base_url=agent_url)

            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are Philippe Brule, CTO and co-founder of restack : the entreprise-grade backend framework to help develoeprs build reliable and accurate AI agents. You live in San Francisco, California."
                    ),
                },
            ]

            context = OpenAILLMContext(messages)
            context_aggregator = llm.create_context_aggregator(context)

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
                ]
            )

            task = PipelineTask(
                pipeline,
                params=PipelineParams(
                    audio_in_sample_rate=16000,
                    audio_out_sample_rate=16000,
                    allow_interruptions=True,
                    enable_metrics=True,
                    enable_usage_metrics=True,
                    report_only_initial_ttfb=True,
                ),
            )

            @transport.event_handler("on_participant_joined")
            async def on_participant_joined(
                transport: DailyTransport, participant: Mapping[str, Any]
            ) -> None:
                # Ignore the Tavus replica's microphone
                if participant.get("info", {}).get("userName", "") == persona_name:
                    log.debug(f"Ignoring {participant['id']}'s microphone")
                    await transport.update_subscriptions(
                        participant_settings={
                            participant["id"]: {
                                "media": {"microphone": "unsubscribed"},
                            }
                        }
                    )
                else:
                    messages.append(
                        {
                            "role": "system",
                            "content": "Please introduce yourself to the user. Keep it short and concise.",
                        }
                    )
                    await task.queue_frames(
                        [context_aggregator.user().get_context_frame()]
                    )

            @transport.event_handler("on_participant_left")
            async def on_participant_left(transport, participant, reason):
                await task.cancel()

            runner = PipelineRunner()

            async def run_pipeline() -> None:
                try:
                    await runner.run(task)
                except Exception as e:
                    error_message = "Pipeline runner encountered an error, cancelling pipeline"
                    log.error(error_message, error=e)
                    # Cancel the pipeline task if an error occurs within the pipeline runner.
                    await task.cancel()
                    raise NonRetryableError(error_message) from e

            # Launch the pipeline runner as a background task so it doesn't block the return.
            asyncio.create_task(run_pipeline())

            log.info("Pipecat pipeline started", room_url=room_url)

            # Return the room_url immediately.
            return room_url
    except Exception as e:
        error_message = "Pipecat pipeline failed"
        log.error(error_message, error=e)
        raise NonRetryableError(error_message) from e
