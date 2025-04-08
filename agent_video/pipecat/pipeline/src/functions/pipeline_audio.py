import os

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
from restack_ai.function import (
    NonRetryableError,
    function,
    log,
)

load_dotenv(override=True)


class PipecatPipelineAudioInput(BaseModel):
    agent_name: str
    agent_id: str
    agent_run_id: str
    daily_room_url: str
    daily_room_token: str


VOICE_IDS = {
    "system_1": os.getenv("CARTESIA_VOICE_ID"),  # Restack voice
    "system_2": os.getenv(
        "CARTESIA_VOICE_ID_SYSTEM_2"
    ),  # Female voice
}


def get_agent_backend_host(engine_api_address: str) -> str:
    if not engine_api_address:
        return "http://localhost:9233"
    if not engine_api_address.startswith("https://"):
        return "https://" + engine_api_address
    return engine_api_address


@function.defn(name="pipecat_pipeline_audio")
async def pipecat_pipeline_audio(
    function_input: PipecatPipelineAudioInput,
) -> bool:
    try:
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
            bot_name="bot",
            params=DailyParams(
                audio_in_enabled=True,
                audio_out_enabled=True,
                transcription_enabled=True,
                camera_out_enabled=False,
                vad_enabled=True,
                vad_analyzer=SileroVADAnalyzer(),
                vad_audio_passthrough=True,
            ),
        )

        stt = DeepgramSTTService(
            api_key=os.getenv("DEEPGRAM_API_KEY"),
        )

        tts = CartesiaTTSService(
            api_key=os.getenv("CARTESIA_API_KEY"),
            voice_id=VOICE_IDS["system_1"],
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
            context
        )

        pipeline = Pipeline(
            [
                transport.input(),  # Transport user input
                stt,  # STT
                context_aggregator.user(),  # User responses
                llm,  # LLM
                tts,  # TTS
                transport.output(),  # Transport bot output,
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
            check_dangling_tasks=True,
        )

        @transport.event_handler(
            "on_first_participant_joined",
        )
        async def on_first_participant_joined(
            transport: DailyTransport,
            participant: dict,
        ) -> None:
            log.info(
                "First participant joined",
                participant=participant,
            )

            messages.append(
                {
                    "role": "system",
                    "content": "Please introduce yourself to the user.",
                }
            )
            await task.queue_frames(
                [context_aggregator.user().get_context_frame()]
            )

        @transport.event_handler("on_app_message")
        async def on_app_message(transport, message, sender):
            text = message.get("text")
            log.info(f"Received {sender} message with {text}")
            try:
                tts.set_voice(VOICE_IDS["system_2"])
                await tts.say(f"SYSTEM TWO: {text}")
                tts.set_voice(VOICE_IDS["system_1"])
            except Exception as e:
                log.error("Error processing message", error=e)

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

        try:
            await runner.run(task)
        except Exception as e:
            log.error(
                "Pipeline runner error, cancelling pipeline",
                error=e,
            )
            await task.cancel()
            raise NonRetryableError(
                "Pipeline runner error, cancelling pipeline"
            ) from e

        return True
    except Exception as e:
        error_message = "Pipecat pipeline failed"
        log.error(error_message, error=e)
        raise NonRetryableError(error_message) from e
