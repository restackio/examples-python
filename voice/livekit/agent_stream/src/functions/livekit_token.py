from dataclasses import dataclass
import os
import secrets
from livekit import api
from restack_ai.function import function, log, function_info

@dataclass
class LivekitTokenInput:
    agent_name: str
    agent_id: str
    run_id: str

@dataclass
class LivekitTokenOutput:
    ws_url: str
    token: str
    agent_name: str
    agent_id: str
    run_id: str

@function.defn()
async def livekit_token(function_input: LivekitTokenInput):
    
    try:

        participant_identity = f"voice_assistant_user_{secrets.randbelow(10_000)}"

        token = api.AccessToken(os.getenv('LIVEKIT_API_KEY'), os.getenv('LIVEKIT_API_SECRET')) \
        .with_identity("identity") \
        .with_name(participant_identity) \
        .with_grants(api.VideoGrants(
            room_join=True,
            room=function_input.run_id,
        ))
        return {
            "ws_url": os.getenv('LIVEKIT_URL'),
            "token": token.to_jwt(),
            "agent_name": function_input.agent_name,
            "agent_id": function_input.agent_id,
            "run_id": function_input.run_id
        }

    except Exception as e:
        log.error("livekit_dispatch function failed", error=str(e))
        raise e