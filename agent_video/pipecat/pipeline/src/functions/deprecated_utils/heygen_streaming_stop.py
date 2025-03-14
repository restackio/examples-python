import os

import requests
from dotenv import load_dotenv
from pydantic import BaseModel
from restack_ai.function import NonRetryableError, function, log

# Load environment variables from .env file
load_dotenv()


class HeygenStreamingStopInput(BaseModel):
    session_id: str


@function.defn(name="heygen_streaming_stop")
async def heygen_streaming_stop(
    function_input: HeygenStreamingStopInput,
) -> bool:
    try:
        api_key = os.getenv("HEYGEN_API_KEY")
        if not api_key:
            raise ValueError(
                "HEYGEN_API_KEY not set in environment.",
            )

        url = "https://api.heygen.com/v1/streaming.stop"
        payload = {
            "session_id": function_input.session_id,
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "x-api-key": api_key,
        }

        response = requests.post(
            url,
            json=payload,
            headers=headers,
        )
        if response.status_code != 200:
            raise NonRetryableError(
                f"Error: Received status code {response.status_code} with details: {response.text}",
            )

        message = response.json().get("message", {})

        log.info("Heygen streaming session stop", message=message)

        if message == "success":
            return True
        return False
    except Exception as e:
        raise NonRetryableError(
            f"heygen_streaming_session error: {e}",
        ) from e
