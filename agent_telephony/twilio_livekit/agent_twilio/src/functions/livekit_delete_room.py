import os

from livekit import api
from livekit.api import DeleteRoomRequest, DeleteRoomResponse
from restack_ai.function import (
    NonRetryableError,
    function,
    function_info,
)


@function.defn()
async def livekit_delete_room() -> DeleteRoomResponse:
    try:
        lkapi = api.LiveKitAPI(
            url=os.getenv("LIVEKIT_API_URL"),
            api_key=os.getenv("LIVEKIT_API_KEY"),
            api_secret=os.getenv("LIVEKIT_API_SECRET"),
        )

        run_id = function_info().workflow_run_id

        deleted_room = await lkapi.room.delete_room(
            DeleteRoomRequest(room=run_id)
        )

        await lkapi.aclose()

    except Exception as e:
        error_message = (
            f"livekit_delete_room function failed: {e}"
        )
        raise NonRetryableError(error_message) from e

    else:
        return deleted_room
