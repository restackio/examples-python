"""Utils.

Provides utility functions and a shared logger configuration for the LiveKit pipeline example project.
"""

import asyncio
import json
import logging
import os
from typing import Any

# Configure shared logger with a consistent format across modules.
logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(asctime)s - %(name)s - %(message)s",
)
logger = logging.getLogger("livekit_pipeline")

pending_tasks: list[asyncio.Task] = []


def track_task(task: asyncio.Task) -> None:
    """Track an asyncio task by adding it to the global list `pending_tasks`.

    The task is removed automatically once completed.

    Args:
        task (asyncio.Task): The task to track.

    """
    pending_tasks.append(task)

    def remove_task(t: asyncio.Task) -> None:
        try:
            pending_tasks.remove(t)
        except ValueError:
            logger.warning("Task not found in pending_tasks list")

    task.add_done_callback(remove_task)


def parse_metadata(metadata: Any) -> Any:
    """Parse job metadata from a JSON string or return as-is if already parsed.

    Args:
        metadata (Any): The metadata to parse.

    Returns:
        Any: The parsed JSON object or the original metadata.

    """
    if isinstance(metadata, str):
        try:
            return json.loads(metadata)
        except json.JSONDecodeError:
            try:
                normalized = metadata.replace("'", '"')
                return json.loads(normalized)
            except json.JSONDecodeError as norm_error:
                logger.warning(
                    "Normalization failed, using default values: %s",
                    norm_error,
                )
                return {}
        except Exception:
            logger.exception("Unexpected error parsing metadata")
            return {}
    return metadata


def extract_agent_info(
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


def get_agent_backend_host() -> str:
    """Retrieve the backend host URL from environment variables.

    Defaults to "http://localhost:9233" if not provided.

    Returns:
        str: The backend host URL.

    """
    engine_api_address = os.environ.get(
        "RESTACK_ENGINE_API_ADDRESS"
    )
    if not engine_api_address:
        return "http://localhost:9233"
    if not engine_api_address.startswith("https://"):
        return "https://" + engine_api_address
    return engine_api_address
