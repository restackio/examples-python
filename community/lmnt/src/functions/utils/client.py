"""Client module for LMNT API integration."""

import os

from dotenv import load_dotenv
from lmnt.api import Speech

load_dotenv()


async def lmnt_client() -> Speech:
    """Initialize and return LMNT Speech client.

    Raises:
        ValueError: If LMNT_API_KEY environment variable is not set
        RuntimeError: If client initialization fails

    """
    api_key = os.getenv("LMNT_API_KEY")
    if not api_key:
        error_message = "LMNT_API_KEY environment variable is not set"
        raise ValueError(error_message)
    try:
        return Speech(api_key)
    except Exception as e:
        error_message = "Failed to initialize LMNT client: %s"
        raise RuntimeError(error_message) from e
