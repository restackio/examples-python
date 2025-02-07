"""Module for LMNT speech synthesis functionality."""

from typing import Any

from restack_ai.function import FunctionFailure, function, log

from .utils.client import lmnt_client


@function.defn()
async def lmnt_list_voices() -> dict[str, Any]:
    client = None
    try:
        client = await lmnt_client()
        voices = await client.list_voices()
    except Exception as e:
        error_message = "Failed to list voices: %s"
        log.error(error_message, error=e)
        raise FunctionFailure(error_message, non_retryable=True) from e
    else:
        return {"voices": voices}
    finally:
        if client and hasattr(client, "close"):
            await client.close()
