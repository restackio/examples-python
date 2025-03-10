"""Env Check.

This module checks that all required environment variables are set.
It is intended to be used during application startup to warn developers about missing configurations.
"""

import os
from dotenv import load_dotenv
from src.utils import logger  # Using the shared logger from utils

REQUIRED_ENVS: dict[str, str] = {
    "LIVEKIT_URL": "LiveKit server URL",
    "LIVEKIT_API_KEY": "API Key for LiveKit",
    "LIVEKIT_API_SECRET": "API Secret for LiveKit",
    "DEEPGRAM_API_KEY": "API key for Deepgram (used for STT)",
    "ELEVEN_API_KEY": "API key for ElevenLabs (used for TTS)",
}


# Load environment variables from the .env file.
load_dotenv(dotenv_path=".env")

def check_env_vars() -> None:
    """Check required environment variables and log warnings if any are missing."""
    try:
        for key, description in REQUIRED_ENVS.items():
            if not os.environ.get(key):
                logger.warning(
                    "Environment variable '%s' (%s) is not set.",
                    key,
                    description,
                )
        logger.info("Environment variable check complete.")
    except Exception as e:
        logger.exception(
            "Error during environment variable check: %s", e
        )
        raise
