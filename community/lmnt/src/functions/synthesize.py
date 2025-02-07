"""Module for LMNT speech synthesis functionality."""

from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field
from restack_ai.function import FunctionFailure, function, log

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
        media_path = Path("src/media")
        media_path.mkdir(parents=True, exist_ok=True)
        file_path = media_path / params.filename
        with file_path.open("wb") as f:
            f.write(synthesis["audio"])
    except Exception as e:
        error_message = "Synthesis failed: %s"
        log.error(error_message, error=e)
        raise FunctionFailure(error_message) from e
    else:
        return params.filename
    finally:
        if client and hasattr(client, "close"):
            await client.close()
