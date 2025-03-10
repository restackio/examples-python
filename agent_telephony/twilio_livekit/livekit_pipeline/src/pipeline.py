"""Pipeline.

This module provides functions to create and configure LiveKit pipeline.
"""

from livekit.agents import JobContext
from livekit.agents.pipeline import VoicePipelineAgent
from livekit.plugins import (
    deepgram,
    elevenlabs,
    openai,
    turn_detector,
)
from src.utils import logger


def create_livekit_pipeline(
    ctx: JobContext, agent_id: str, agent_url: str
) -> VoicePipelineAgent:
    """Create and configure a VoicePipelineAgent with the provided context, agent_id, and agent_url.

    Args:
        ctx (JobContext): The job context containing user data and configuration.
        agent_id (str): The identifier for the agent.
        agent_url (str): The URL for the agent backend.

    Returns:
        VoicePipelineAgent: A configured agent instance.
    """
    try:
        logger.info(
            "Creating VoicePipelineAgent with agent_id: %s and agent_url: %s",
            agent_id,
            agent_url,
        )
        return VoicePipelineAgent(
            vad=ctx.proc.userdata["vad"],
            stt=deepgram.STT(
                model="nova-3-general",
            ),
            llm=openai.LLM(
                api_key=f"{agent_id}-livekit",
                base_url=agent_url,
            ),
            tts=elevenlabs.TTS(
                voice=elevenlabs.tts.Voice(
                    id="UgBBYS2sOqTuMpoF3BR0",
                    name="Mark",
                    category="premade",
                    settings=elevenlabs.tts.VoiceSettings(
                        stability=0,
                        similarity_boost=0,
                        style=0,
                        speed=1.01,
                        use_speaker_boost=False
                    ),
                ),
            ),
            turn_detector=turn_detector.EOUModel(),
        )
    except Exception as e:
        logger.exception(
            "Error creating VoicePipelineAgent: %s", e
        )
        raise
