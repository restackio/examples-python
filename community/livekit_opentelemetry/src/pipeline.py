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
from src.otel_provider import record_metrics
from src.otel_exporter import setup_google_cloud_exporter

# Set up the Google Cloud exporter
setup_google_cloud_exporter()

# Load environment variables from .env
load_dotenv(dotenv_path=".env")

# Setup basic logging configuration so that all logs are properly output.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize total variables at the beginning of the function or module
# These should be initialized at the module level if they need to persist across multiple calls

total_llm_prompt_tokens = 0
# Initialize other total variables similarly

total_llm_completion_tokens = 0
total_tts_characters_count = 0
total_stt_audio_duration = 0

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


# Validate environments at module load
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

    # Retrieve the Host from environment variables.
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

    # Wait for the first participant to connect
    participant = await ctx.wait_for_participant()
    logger.info("Starting voice assistant for participant: %s", participant.identity)

    agent = VoicePipelineAgent(
        vad=ctx.proc.userdata["vad"],
        stt=deepgram.STT(),
        llm=openai.LLM(
            # model="gpt-4o-mini",
            # api_key=os.environ.get("OPENAI_API_KEY"),
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

    async def send_pipeline_metrics(summary: str) -> None:
        logger.warning("Sending pipeline metrics")
        

    @agent.on("metrics_collected")
    def on_metrics_collected(agent_metrics: metrics.AgentMetrics) -> None:
        record_metrics(agent_metrics)
        
    usage_collector.get_summary()

    agent.start(ctx.room, participant)


if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            agent_name="AgentTelemetry",
            prewarm_fnc=prewarm,
        )
    )
