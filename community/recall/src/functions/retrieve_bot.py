from restack_ai.function import function, FunctionFailure, log
from pydantic import BaseModel
import requests
from typing import Optional
import os

class RetrieveBotInput(BaseModel):
    bot_id: str

@function.defn()
async def retrieve_bot(input: RetrieveBotInput) -> dict:
    try:
        headers = {
            "Authorization": f"Token {os.getenv('RECALL_API_KEY')}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(
            f"https://api.recall.ai/api/v1/bot/{input.bot_id}",
            headers=headers
        )
        
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.RequestException as e:
        log.error(f"Failed to retrieve bot: {e}")
        raise FunctionFailure(f"Failed to retrieve bot: {e}", non_retryable=True) from e
    except Exception as e:
        log.error(f"Unexpected error retrieving bot: {e}")
        raise FunctionFailure(f"Unexpected error: {e}", non_retryable=True) from e