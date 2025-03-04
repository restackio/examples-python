import os
from dataclasses import dataclass

from livekit import api
from livekit.protocol.agent_dispatch import AgentDispatch
from restack_ai.function import NonRetryableError, function, function_info


@dataclass
class LivekitDispatchInput:
    room_id: str | None = None


@function.defn()
async def livekit_dispatch(function_input: LivekitDispatchInput) -> AgentDispatch:
    try:
        lkapi = api.LiveKitAPI(
            url=os.getenv("LIVEKIT_API_URL"),
            api_key=os.getenv("LIVEKIT_API_KEY"),
            api_secret=os.getenv("LIVEKIT_API_SECRET"),
        )

        agent_name = function_info().workflow_type
        agent_id = function_info().workflow_id
        run_id = function_info().workflow_run_id

        metadata = {"agent_name": agent_name, "agent_id": agent_id, "run_id": run_id}

        room = function_input.room_id or run_id

        dispatch = await lkapi.agent_dispatch.create_dispatch(
            api.CreateAgentDispatchRequest(
                agent_name=agent_name, room=room, metadata=str(metadata)
            )
        )

        await lkapi.aclose()

    except Exception as e:
        error_message = "Livekit dispatch failed"
        raise NonRetryableError(error_message) from e

    else:
        return dispatch
