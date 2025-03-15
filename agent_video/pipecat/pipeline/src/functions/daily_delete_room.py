import os

import aiohttp
from dotenv import load_dotenv
from pipecat.transports.services.helpers.daily_rest import (
    DailyRESTHelper,
)
from pydantic import BaseModel
from restack_ai.function import (
    NonRetryableError,
    function,
    log,
)

# Load environment variables from .env file
load_dotenv()

class DailyDeleteRoomInput(BaseModel):
    room_name: str

@function.defn(name="daily_delete_room")
async def daily_delete_room(
    function_input: DailyDeleteRoomInput,
) -> bool:
    try:
        
        api_key = os.getenv("DAILYCO_API_KEY")
        if not api_key:
            raise ValueError(
                "DAILYCO_API_KEY not set in environment.",
            )

        async with aiohttp.ClientSession() as daily_session:
            daily_rest_helper = DailyRESTHelper(
                daily_api_key=api_key,
                daily_api_url="https://api.daily.co/v1",
                aiohttp_session=daily_session,
            )

            deleted_room = await daily_rest_helper.delete_room_by_name(function_input.room_name)

            log.info("daily_room deleted", deleted_room=deleted_room)
            return deleted_room

    except Exception as e:
        log.error("Error deleting daily room", error=e)
        raise NonRetryableError(
            f"Error deleting daily room: {e}",
        ) from e
