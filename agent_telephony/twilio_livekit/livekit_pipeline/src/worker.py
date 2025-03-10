"""Worker.

This is the main entrypoint to run the LiveKit worker.
It orchestrates connection to a LiveKit room, agent creation, and
event handling for incoming data.
"""

import asyncio
from typing import Any

from livekit.agents import (
    AutoSubscribe,
    JobContext,
    JobProcess,
    WorkerOptions,
    cli,
    metrics,
)
from livekit.plugins import silero
from src.env_check import check_env_vars
from src.metrics import setup_pipeline_metrics
from src.pipeline import create_livekit_pipeline
from src.restack.utils import (
    extract_restack_agent_info,
    get_restack_agent_url,
)
from src.utils import (
    logger,
    parse_metadata,
    track_task,
)


def prewarm(proc: JobProcess) -> None:
    """Prewarm the system by loading necessary models before the agent starts."""
    logger.info("Prewarming: loading VAD model...")
    proc.userdata["vad"] = silero.VAD.load()
    logger.info("VAD model loaded successfully.")


async def entrypoint(ctx: JobContext) -> None:
    """Run main entrypoint for LiveKit.

    Processes job metadata, checks environment variables, sets up the agent and metrics,
    and starts the data handling for the LiveKit room.
    """
    # Check environment variables and log warnings if any are missing.
    check_env_vars()

    # Extract metadata to match pipeline with Restack agent

    metadata = ctx.job.metadata
    logger.info("Job metadata: %s", metadata)
    metadata_obj = parse_metadata(metadata)
    agent_name, agent_id, run_id = extract_restack_agent_info(
        metadata_obj
    )
    agent_url = get_restack_agent_url(
        agent_name, agent_id, run_id
    )

    logger.info("Restack agent url: %s", agent_url)

    # Connect to LiveKit room

    logger.info("Connecting to room: %s", ctx.room.name)

    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    participant = await ctx.wait_for_participant()

    logger.info(
        "Starting voice assistant for participant: %s",
        participant.identity,
    )

    pipeline = create_livekit_pipeline(ctx, agent_id, agent_url)

    # Setup metrics

    usage_collector = metrics.UsageCollector()

    setup_pipeline_metrics(
        pipeline, agent_id, run_id, usage_collector
    )

    usage_collector.get_summary()

    # Allow pipeline to speak when receiving data

    async def say(text: str) -> None:
        """Send a text message to the pipeline's TTS system.

        Args:
            text (str): The text to be spoken in the pipeline.

        """
        await pipeline.say(text)

    @ctx.room.on("data_received")
    def on_data_received(data_packet: Any) -> None:
        """Handle data received in the LiveKit room.

        Decode data and pass it to the pipeline for processing.

        Args:
            data_packet (Any): The incoming data packet.

        """
        logger.info("Received data: %s", data_packet)
        byte_content = data_packet.data
        if isinstance(byte_content, bytes):
            text_data = byte_content.decode("utf-8")
            logger.info("Text data: %s", text_data)
            track_task(asyncio.create_task(say(text_data)))
        else:
            logger.warning("Data is not in bytes format.")

    # Start pipeline and welcome user

    pipeline.start(ctx.room, participant)

    logger.info("Pipeline started", ctx.job.metadata)

    welcome_message = (
        "Welcome to restack, how can I help you today?"
    )

    await pipeline.say(welcome_message, allow_interruptions=True)


if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            agent_name="AgentTwilio",
            prewarm_fnc=prewarm,
        )
    )
