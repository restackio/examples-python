from restack_ai.function import function, FunctionFailure, log
from pydantic import BaseModel
import requests
from typing import Optional
import os

class CreateMeetBotInput(BaseModel):
    meeting_url: str = "https://meet.google.com/jgv-jvev-jhe"
    bot_name: Optional[str] = "Recall Bot"
    transcription_options: Optional[dict] = { "provider": "meeting_captions" }

@function.defn()
async def create_meet_bot(input: CreateMeetBotInput) -> dict:
    try:
        headers = {
            "Authorization": f"Token {os.getenv('RECALL_API_KEY')}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "meeting_url": input.meeting_url,
            "transcription_options": input.transcription_options,
            "bot_name": input.bot_name,
            "google_meet": {
                "login_required": False
            }
        }
        
        response = requests.post(
            "https://us-west-2.recall.ai/api/v1/bot",
            headers=headers,
            json=payload
        )
        
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.RequestException as e:
        log.error(f"Failed to create meet bot: {e}")
        raise FunctionFailure(f"Failed to create meet bot: {e}", non_retryable=True) from e
    except Exception as e:
        log.error(f"Unexpected error creating meet bot: {e}")
        raise FunctionFailure(f"Unexpected error: {e}", non_retryable=True) from e