import asyncio
import json
import logging
import os

from dotenv import load_dotenv
from livekit.agents import (
    AutoSubscribe,
    JobContext,
    JobProcess,
    WorkerOptions,
    cli,
    metrics,
)
from livekit.agents.pipeline import VoicePipelineAgent
from livekit.plugins import deepgram, elevenlabs, openai, silero, turn_detector
from src.client import client

load_dotenv(dotenv_path=".env")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def validate_envs() -> None:
    required_envs = {
        "LIVEKIT_URL": "LiveKit server URL",
        "LIVEKIT_API_KEY": "API Key for LiveKit",
        "LIVEKIT_API_SECRET": "API Secret for LiveKit",
        "DEEPGRAM_API_KEY": "API key for Deepgram (used for STT)",
        "ELEVEN_API_KEY": "API key for ElevenLabs (used for TTS)",
    }
    for key, description in required_envs.items():
        if not os.environ.get(key):
            logger.warning("Environment variable %s (%s) is not set.", key, description)


validate_envs()


def prewarm(proc: JobProcess) -> None:
    logger.info("Prewarming: loading VAD model...")
    proc.userdata["vad"] = silero.VAD.load()
    logger.info("VAD model loaded successfully.")


async def entrypoint(ctx: JobContext) -> None:
    metadata = ctx.job.metadata

    logger.info("job metadata: %s", metadata)

    if isinstance(metadata, str):
        try:
            metadata_obj = json.loads(metadata)
        except json.JSONDecodeError:
            try:
                normalized = metadata.replace("'", '"')
                metadata_obj = json.loads(normalized)
            except json.JSONDecodeError as norm_error:
                logger.warning(
                    "Normalization failed, using default values: %s", norm_error
                )
                metadata_obj = {}
    else:
        metadata_obj = metadata

    logger.info("metadata_obj: %s", metadata_obj)

    agent_name = metadata_obj.get("agent_name")
    agent_id = metadata_obj.get("agent_id")
    run_id = metadata_obj.get("run_id")

    engine_api_address = os.environ.get("RESTACK_ENGINE_API_ADDRESS")
    if not engine_api_address:
        agent_backend_host = "http://localhost:9233"
    elif not engine_api_address.startswith("https://"):
        agent_backend_host = "https://" + engine_api_address
    else:
        agent_backend_host = engine_api_address

    logger.info("Using RESTACK_ENGINE_API_ADDRESS: %s", agent_backend_host)

    agent_url = f"{agent_backend_host}/stream/agents/{agent_name}/{agent_id}/{run_id}"
    logger.info("Agent URL: %s", agent_url)

    logger.info("Connecting to room: %s", ctx.room.name)
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    participant = await ctx.wait_for_participant()
    logger.info("Starting voice assistant for participant: %s", participant.identity)

    agent = VoicePipelineAgent(
        vad=ctx.proc.userdata["vad"],
        stt=deepgram.STT(),
        llm=openai.LLM(
            api_key=f"{agent_id}-livekit",
            base_url=agent_url,
        ),
        tts=elevenlabs.TTS(),
        turn_detector=turn_detector.EOUModel(),
        # minimum delay for endpointing, used when turn detector believes the user is done with their turn
        # min_endpointing_delay=0.5,
        # # maximum delay for endpointing, used when turn detector does not believe the user is done with their turn
        # max_endpointing_delay=5.0,
    )

    usage_collector = metrics.UsageCollector()

    @agent.on("metrics_collected")
    def on_metrics_collected(agent_metrics: metrics.AgentMetrics) -> None:
        metrics.log_metrics(agent_metrics)

        async def send_metrics(agent_metrics):
            try:
                latencies = []
                if isinstance(agent_metrics, metrics.PipelineEOUMetrics):
                    total_latency = agent_metrics.end_of_utterance_delay
                    latencies.append(total_latency * 1000)

                elif isinstance(agent_metrics, metrics.PipelineLLMMetrics):
                    total_latency = agent_metrics.ttft
                    latencies.append(total_latency * 1000)

                elif isinstance(agent_metrics, metrics.PipelineTTSMetrics):
                    total_latency = agent_metrics.ttfb
                    latencies.append(total_latency * 1000)

                if latencies:
                    metrics_latencies = str(json.dumps({"latencies": latencies}))
                    logger.info(f"Sending pipeline metrics: {metrics_latencies!s}")

                    await client.send_agent_event(
                        event_name="pipeline_metrics",
                        agent_id=agent_id.replace("local-", ""),
                        run_id=run_id,
                        event_input={
                            "metrics": agent_metrics,
                            "latencies": metrics_latencies,
                        },
                    )
            except Exception as e:
                logger.error("Error sending pipeline metrics", error=e)

        asyncio.create_task(send_metrics(agent_metrics))

        usage_collector.collect(agent_metrics)

    usage_collector.get_summary()

    async def say(text: str):
        await agent.say(text)

    @ctx.room.on("data_received")
    def on_data_received(data_packet) -> None:
        logger.info(f"Received data: {data_packet}")

        byte_content = data_packet.data
        if isinstance(byte_content, bytes):
            text_data = byte_content.decode("utf-8")
            logger.info(f"Text data: {text_data}")

            asyncio.create_task(say(text_data))

        else:
            logger.warning("Data is not in bytes format.")

    agent.start(ctx.room, participant)

    await asyncio.sleep(0.1)

    await agent.say(
        "Welcome to restack, how can I help you today?", allow_interruptions=True
    )


if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            agent_name="AgentTwilio",
            prewarm_fnc=prewarm,
        )
    )
