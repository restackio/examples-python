from typing import Any

from pydantic import BaseModel
from restack_ai.function import NonRetryableError, function

from src.client import client


class SendAgentEventInput(BaseModel):
    event_name: str
    agent_id: str
    run_id: str | None = None
    event_input: dict[str, Any] | None = None


@function.defn()
async def send_agent_event(
    function_input: SendAgentEventInput,
) -> str:
    try:
        return await client.send_agent_event(
            event_name=function_input.event_name,
            agent_id=function_input.agent_id,
            run_id=function_input.run_id,
            event_input=function_input.event_input,
        )

    except Exception as e:
        raise NonRetryableError(
            f"send_agent_event failed: {e}"
        ) from e
