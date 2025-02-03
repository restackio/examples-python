"""Module for LMNT speech synthesis functionality."""

import os
from typing import Any

from pydantic import BaseModel, Field
from restack_ai.function import FunctionFailure, function

from .utils.client import lmnt_client


class SynthesizeInputParams(BaseModel):
    user_content: str = Field(description="The text content to synthesize")
    voice: str = Field(description="The voice to use for synthesis")
    filename: str = Field(description="The output filename")
    options: dict[str, Any] | None = Field(
        default=None,
        description="Optional synthesis parameters",
    )


@function.defn()
async def lmnt_synthesize(params: SynthesizeInputParams) -> str:
    client = None
    try:
        client = await lmnt_client()
        synthesis = await client.synthesize(params.user_content, params.voice)
        media_path = os.path.join("src", "media")
        os.makedirs(media_path, exist_ok=True)
        file_path = os.path.join(media_path, params.filename)
        with open(file_path, "wb") as f:
            f.write(synthesis["audio"])
        return params.filename
    except Exception as e:
        raise FunctionFailure(f"Synthesis failed: {e!s}") from e
    finally:
        if client and hasattr(client, "close"):
            await client.close()
