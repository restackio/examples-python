from restack_ai.function import function, FunctionFailure, log
from pydantic import BaseModel
import requests
from typing import Optional
import os

class ListBotsInput(BaseModel):
    limit: Optional[int] = None
    offset: Optional[int] = None

@function.defn()
async def list_bots(input: ListBotsInput) -> dict:
    try:
        headers = {
            "Authorization": f"Token {os.getenv('RECALL_API_KEY')}",
            "Content-Type": "application/json"
        }
        
        params = {}
        if input.limit is not None:
            params["limit"] = input.limit
        if input.offset is not None:
            params["offset"] = input.offset
            
        response = requests.get(
            "https://us-west-2.recall.ai/api/v1/bot/",
            headers=headers,
            params=params
        )
        
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.RequestException as e:
        log.error(f"Failed to list bots: {e}")
        raise FunctionFailure(f"Failed to list bots: {e}", non_retryable=True) from e
    except Exception as e:
        log.error(f"Unexpected error listing bots: {e}")
        raise FunctionFailure(f"Unexpected error: {e}", non_retryable=True) from e