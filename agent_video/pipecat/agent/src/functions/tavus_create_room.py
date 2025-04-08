import os

import aiohttp
from dotenv import load_dotenv
from pydantic import BaseModel
from restack_ai.function import (
    NonRetryableError,
    function,
    log,
)

# Load environment variables from .env file
load_dotenv()


class TavusRoomOutput(BaseModel):
    room_url: str


@function.defn(name="tavus_create_room")
async def tavus_create_room() -> TavusRoomOutput:
    try:
        api_key = os.getenv("TAVUS_API_KEY")
        replica_id = os.getenv("TAVUS_REPLICA_ID")
        if not api_key or not replica_id:
            raise ValueError(
                "TAVUS_API_KEY or TAVUS_REPLICA_ID not set in environment.",
            )

        async with aiohttp.ClientSession() as session:
            url = "https://tavusapi.com/v2/conversations"
            headers = {
                "Content-Type": "application/json",
                "x-api-key": api_key,
            }
            payload = {
                "replica_id": replica_id,
                "persona_id": "pipecat0",
            }

            async with session.post(
                url, headers=headers, json=payload
            ) as r:
                r.raise_for_status()
                response_json = await r.json()

            log.info("Tavus room created", response=response_json)
            return TavusRoomOutput(
                room_url=response_json["conversation_url"],
            )

    except Exception as e:
        log.error("Error creating Tavus room", error=e)
        raise NonRetryableError(
            f"Error creating Tavus room: {e}",
        ) from e
