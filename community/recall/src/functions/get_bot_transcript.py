from restack_ai.function import function, FunctionFailure, log
from pydantic import BaseModel
import requests
from typing import Optional
import os

class GetBotTranscriptInput(BaseModel):
    bot_id: str

@function.defn()
async def get_bot_transcript(input: GetBotTranscriptInput) -> dict:
    try:
        headers = {
            "Authorization": f"Token {os.getenv('RECALL_API_KEY')}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(
            f"https://us-west-2.recall.ai/api/v1/bot/{input.bot_id}/transcript/",
            headers=headers
        )
        
        response.raise_for_status()
        return {"segments": response.json()}
        
    except requests.exceptions.RequestException as e:
        log.error(f"Failed to get bot transcript: {e}")
        raise FunctionFailure(f"Failed to get bot transcript: {e}", non_retryable=True) from e
    except Exception as e:
        log.error(f"Unexpected error getting bot transcript: {e}")
        raise FunctionFailure(f"Unexpected error: {e}", non_retryable=True) from e