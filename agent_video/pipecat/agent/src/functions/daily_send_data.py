import os

import aiohttp
from dotenv import load_dotenv
from pydantic import BaseModel
from restack_ai.function import (
    NonRetryableError,
    function,
    log,
)

load_dotenv()

async def send_data_to_room(room_name: str, data: dict, recipient: str | None = "*") -> bool:
    """Send a message to a Daily room."""
    api_key = os.getenv("DAILYCO_API_KEY")
    if not api_key:
        raise ValueError("DAILYCO_API_KEY not set in environment.")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    url = f"https://api.daily.co/v1/rooms/{room_name}/send-app-message"
    recipient = recipient or "*"
    data = {
        "data": data,
        "recipient": recipient
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            if response.status != 200:
                text = await response.text()
                raise Exception(f"Failed to send message (status: {response.status}): {text}")

    return True


class DailySendDataInput(BaseModel):
    room_url: str
    data: dict
    recipient: str | None = "*"

@function.defn(name="daily_send_data")
async def daily_send_data(
    function_input: DailySendDataInput,
) -> bool:
    try:
        return await send_data_to_room(
            room_name=function_input.room_url.split('/')[-1],
            data=function_input.data,
            recipient=function_input.recipient
        )
    except Exception as e:
        log.error("Error sending message to daily room", error=e)
        raise NonRetryableError(
            f"Error sending message to daily room: {e}",
        ) from e
