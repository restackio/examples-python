import os

from dotenv import load_dotenv
from pipecat.transports.services.helpers.daily_rest import (
    DailyRESTHelper,
    DailyRoomParams,
    DailyRoomProperties,
)
from pydantic import BaseModel
from restack_ai.function import (
    NonRetryableError,
    function,
    function_info,
    log,
)

from src.functions.aiohttp_session import get_aiohttp_session

# Load environment variables from .env file
load_dotenv()


class DailyRoomOutput(BaseModel):
    room_url: str
    token: str


class DailyRoomInput(BaseModel):
    room_name: str


@function.defn(name="daily_room")
async def daily_room(
    function_input: DailyRoomInput,
) -> DailyRoomOutput:
    try:
        workflow_run_id = function_info().workflow_run_id
        api_key = os.getenv("DAILYCO_API_KEY")
        if not api_key:
            raise ValueError(
                "DAILYCO_API_KEY not set in environment.",
            )

        session = await get_aiohttp_session(workflow_run_id)
        daily_rest_helper = DailyRESTHelper(
            daily_api_key=api_key,
            daily_api_url="https://api.daily.co/v1",
            aiohttp_session=session,
        )

        room = await daily_rest_helper.create_room(
            params=DailyRoomParams(
                name=function_input.room_name,
                properties=DailyRoomProperties(
                    start_video_off=True,
                    start_audio_off=False,
                    max_participants=2,
                    enable_prejoin_ui=False,
                ),
            ),
        )

        # Create a meeting token for the given room with an expiration 1 hour in
        # the future.
        expiry_time: float = 60 * 60

        token = await daily_rest_helper.get_token(
            room.url,
            expiry_time,
        )

        if not token:
            raise NonRetryableError(
                "No session token found in the response.",
            )

        log.info("daily_room token", token=token)
        return DailyRoomOutput(room_url=room.url, token=token)

    except Exception as e:
        log.error("Error creating daily room", error=e)
        raise NonRetryableError(
            f"Error creating daily room: {e}",
        ) from e
