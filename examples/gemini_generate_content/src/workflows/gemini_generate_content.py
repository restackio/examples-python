from restack_ai.workflow import workflow, workflow_import
from pydantic import BaseModel, Field
from datetime import timedelta

with workflow_import():
    from src.functions.function import gemini_generate_opposite, FunctionInputParams

class WorkflowInputParams(BaseModel):
    user_content: str

@workflow.defn(name="GeminiGenerateOppositeWorkflow")
class GeminiGenerateOppositeWorkflow:
    @workflow.run
    async def run(self, input: WorkflowInputParams):
        return await workflow.step(gemini_generate_opposite, FunctionInputParams(user_content=input.user_content), start_to_close_timeout=timedelta(seconds=10))