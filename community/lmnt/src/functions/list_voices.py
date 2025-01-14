"""Module for LMNT speech synthesis functionality."""
import os
from typing import Dict, Any
from restack_ai.function import function, FunctionFailure
from .utils.client import lmnt_client

@function.defn()
async def lmnt_list_voices() -> Dict[str, Any]:
    client = None
    try:
        client = await lmnt_client()
        voices = await client.list_voices()
        return {"voices": voices}
    except Exception as e:
        raise FunctionFailure(f"Failed to list voices: {str(e)}", non_retryable=True) from e
    finally:
        if client and hasattr(client, 'close'):
            await client.close()