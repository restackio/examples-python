import os

from livekit import api
from pydantic import BaseModel
from restack_ai.function import NonRetryableError, function, log


class LivekitTokenInput(BaseModel):
    room_id: str


@function.defn()
async def livekit_token(function_input: LivekitTokenInput) -> str:
    try:
        token = (
            api.AccessToken(
                os.getenv("LIVEKIT_API_KEY"),
                os.getenv("LIVEKIT_API_SECRET"),
            )
            .with_identity("identity")
            .with_name("dev_user")
            .with_grants(
                api.VideoGrants(
                    room_join=True,
                    room=function_input.room_id,
                )
            )
        )
        log.info("Token generated", token=token.to_jwt())
    except Exception as e:
        error_message = "Error during livekit_token function"
        raise NonRetryableError(message=error_message, error=e) from e

    else:
        return token.to_jwt()
