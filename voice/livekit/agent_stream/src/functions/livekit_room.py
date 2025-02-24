import os

from livekit import api
from livekit.api import CreateRoomRequest, Room
from restack_ai.function import function, function_info, log


@function.defn()
async def livekit_room() -> Room:
    try:
        lkapi = api.LiveKitAPI(
            url=os.getenv("LIVEKIT_API_URL"),
            api_key=os.getenv("LIVEKIT_API_KEY"),
            api_secret=os.getenv("LIVEKIT_API_SECRET"),
        )

        run_id = function_info().workflow_run_id

        room = await lkapi.room.create_room(
            CreateRoomRequest(
                name=run_id,
                empty_timeout=10 * 60,
                max_participants=20,
            )
        )

        await lkapi.aclose()

    except Exception as e:
        log.error("livekit_dispatch function failed", error=str(e))
        raise

    else:
        return room
