from restack_ai import Restack
from restack_ai.function import function, log
from pydantic import BaseModel
from src.client import client
import json

class GetWorkflowMemoryInput(BaseModel):
    workflow_id: str
    run_id: str | None = None
    memory_name: str

@function.defn()
async def get_workflow_memory(input: GetWorkflowMemoryInput):
    try:
        workflow_memory = await client.get_workflow_memory(workflow_id=input.workflow_id.replace('local-', ''),run_id='827beed0-8ef1-4894-8589-423908216194', memory_name=input.memory_name)
        return workflow_memory
    except Exception as e:
        log.error("Failed to get workflow memory", error=str(e), workflow_id=input.workflow_id, run_id=input.run_id, memory_name=input.memory_name)
        raise e
