import aiohttp
from aiohttp import ClientSession

# Add a module-level dictionary for reusing ClientSession keyed by workflow_run_id
SESSIONS: dict[str, ClientSession] = {}

from restack_ai.function import (
    NonRetryableError,
    function,
    function_info,
    log,
)


@function.defn(name="create_aiohttp_session")
async def create_aiohttp_session() -> str:
    try:
        workflow_run_id = function_info().workflow_run_id
        if workflow_run_id not in SESSIONS:
            SESSIONS[workflow_run_id] = aiohttp.ClientSession()
        return workflow_run_id
    except Exception as e:
        log.error("aiohttp_session error", error=e)
        raise NonRetryableError(
            f"aiohttp_session error: {e}",
        ) from e


@function.defn(name="get_aiohttp_session")
async def get_aiohttp_session(
    workflow_run_id: str,
) -> ClientSession:
    """Retrieve the stored aiohttp ClientSession for the given workflow_run_id."""
    try:
        return SESSIONS[workflow_run_id]
    except KeyError:
        log.error(
            "get_aiohttp_session: No session found for workflow_run_id",
            workflow_run_id=workflow_run_id,
        )
        raise NonRetryableError(
            f"No session found for workflow_run_id: {workflow_run_id}",
        )
