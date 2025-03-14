import os

from dotenv import load_dotenv
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


class HeygenStreamingSessionOutput(BaseModel):
    session_id: str
    access_token: str
    realtime_endpoint: str
    url: str


@function.defn(name="heygen_streaming_session")
async def heygen_streaming_session() -> (
    HeygenStreamingSessionOutput
):
    try:
        api_key = os.getenv("HEYGEN_API_KEY")
        if not api_key:
            raise ValueError(
                "HEYGEN_API_KEY not set in environment.",
            )

        session = await get_aiohttp_session(
            function_info().workflow_run_id,
        )

        url = "https://api.heygen.com/v1/streaming.new"
        payload = {
            "avatarName": "Bryan_IT_Sitting_public",
            "version": "v2",
            "video_encoding": "H264",
            "source": "sdk",
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "x-api-key": api_key,
        }

        async with session.post(
            url,
            json=payload,
            headers=headers,
        ) as response:
            if response.status != 200:
                raise NonRetryableError(
                    f"Error: Received status code {response.status} with details: {await response.text()}",
                )
            data = (await response.json()).get("data", {})

        log.info("Heygen streaming session data", data=data)

        session_id = data.get("session_id")
        access_token = data.get("access_token")
        realtime_endpoint = data.get("realtime_endpoint")
        url_value = data.get("url")

        if (
            not session_id
            or not access_token
            or not realtime_endpoint
            or not url_value
        ):
            log.error(
                "Incomplete Heygen streaming session response",
                data=data,
            )
            raise NonRetryableError(
                "Incomplete Heygen streaming session response: missing one of session_id, access_token, realtime_endpoint, or url.",
            )
        return HeygenStreamingSessionOutput(
            session_id=session_id,
            access_token=access_token,
            realtime_endpoint=realtime_endpoint,
            url=url_value,
        )
    except Exception as e:
        raise NonRetryableError(
            f"heygen_streaming_session error: {e}",
        ) from e
