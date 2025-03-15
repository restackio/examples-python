import os

import requests
from dotenv import load_dotenv
from restack_ai.function import NonRetryableError, function, log

# Load environment variables from .env file
load_dotenv()


@function.defn(name="heygen_token")
async def heygen_token():
    api_key = os.getenv("HEYGEN_API_KEY")
    if not api_key:
        raise ValueError("HEYGEN_API_KEY not set in environment.")

    url = "https://api.heygen.com/v1/streaming.create_token"
    payload = {}
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-api-key": api_key,
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        raise NonRetryableError(
            f"Error: Received status code {response.status_code} with details: {response.text}",
        )

    token = response.json().get("data", {}).get("token")
    log.info("Heygen token", token=token)
    if not token:
        raise NonRetryableError(
            "No session token found in the response.",
        )

    return token
