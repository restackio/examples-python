import os

from livekit import api
from livekit.api import SendDataRequest, SendDataResponse
from pydantic import BaseModel
from restack_ai.function import NonRetryableError, function


class LivekitSendDataInput(BaseModel):
    room_id: str
    text: str


@function.defn()
async def livekit_send_data(
    function_input: LivekitSendDataInput,
) -> SendDataResponse:
    try:
        lkapi = api.LiveKitAPI(
            url=os.getenv("LIVEKIT_API_URL"),
            api_key=os.getenv("LIVEKIT_API_KEY"),
            api_secret=os.getenv("LIVEKIT_API_SECRET"),
        )

        send_data_reponse = await lkapi.room.send_data(
            SendDataRequest(
                room=function_input.room_id,
                data=function_input.text.encode("utf-8"),
            )
        )

        await lkapi.aclose()

    except Exception as e:
        error_message = (
            f"livekit_delete_room function failed: {e}"
        )
        raise NonRetryableError(error_message) from e

    else:
        return send_data_reponse
