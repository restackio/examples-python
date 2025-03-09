"""Utils.

Provides utility functions and a shared logger configuration for the LiveKit pipeline example project.
"""

import os
from typing import Any


def extract_restack_agent_info(
    metadata_obj: Any,
) -> tuple[str | None, str | None, str | None]:
    """Extract agent-related information from the metadata object.

    Args:
        metadata_obj (Any): The metadata object.

    Returns:
        tuple[str | None, str | None, str | None]: A tuple of (agent_name, agent_id, run_id).

    """
    return (
        metadata_obj.get("agent_name"),
        metadata_obj.get("agent_id"),
        metadata_obj.get("run_id"),
    )


def get_restack_agent_url(
    agent_name: str, agent_id: str, run_id: str
) -> str:
    """Retrieve the agent base URL.

    Args:
        agent_name (str): The name of the agent.
        agent_id (str): The ID of the agent.
        run_id (str): The run ID of the agent.

    Returns:
        str: The agent base URL.

    """
    engine_api_address = os.environ.get(
        "RESTACK_ENGINE_API_ADDRESS"
    )
    if not engine_api_address:
        hostname = "http://localhost:9233"
    elif not engine_api_address.startswith("https://"):
        hostname = "https://" + engine_api_address
    else:
        hostname = engine_api_address

    return f"{hostname}/stream/agents/{agent_name}/{agent_id}/{run_id}"
