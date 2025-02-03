"""Module for LMNT speech synthesis functionality."""
from typing import Any

from restack_ai.function import FunctionFailure, function

from .utils.client import lmnt_client


@function.defn()
async def lmnt_list_voices() -> dict[str, Any]:
    client = None
    try:
        client = await lmnt_client()
        voices = await client.list_voices()
        return {"voices": voices}
    except Exception as e:
        raise FunctionFailure(f"Failed to list voices: {e!s}", non_retryable=True) from e
    finally:
        if client and hasattr(client, "close"):
            await client.close()
