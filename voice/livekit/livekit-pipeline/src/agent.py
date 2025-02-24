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

load_dotenv(dotenv_path=".env.local")
logger = logging.getLogger("voice-agent")


def prewarm(proc: JobProcess) -> None:
    proc.userdata["vad"] = silero.VAD.load()


async def entrypoint(ctx: JobContext) -> None:
    metadata = ctx.room.metadata

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

    agent_name = metadata_obj.get("agent_name")
    agent_id = metadata_obj.get("agent_id")
    run_id = metadata_obj.get("run_id")

    agent_backend_host = os.environ.get(
        "AGENT_BACKEND_HOST", "http://host.docker.internal:9233"
    )
    agent_url = f"{agent_backend_host}/stream/agents/{agent_name}/{agent_id}/{run_id}"
    logger.info("agent url: %s", agent_url)

    logger.info("connecting to room %s", ctx.room.name)
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    # Wait for the first participant to connect
    participant = await ctx.wait_for_participant()
    logger.info("starting voice assistant for participant %s", participant.identity)

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
        min_endpointing_delay=0.5,
        # maximum delay for endpointing, used when turn detector does not believe the user is done with their turn
        max_endpointing_delay=5.0,
    )

    usage_collector = metrics.UsageCollector()

    @agent.on("metrics_collected")
    def on_metrics_collected(agent_metrics: metrics.AgentMetrics) -> None:
        metrics.log_metrics(agent_metrics)
        usage_collector.collect(agent_metrics)

    agent.start(ctx.room, participant)


if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            agent_name="AgentStream",
            prewarm_fnc=prewarm,
        )
    )
