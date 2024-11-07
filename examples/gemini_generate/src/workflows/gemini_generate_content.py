from restack_ai.workflow import workflow, import_functions
from pydantic import BaseModel
from datetime import timedelta

with import_functions():
    from src.functions.function import gemini_generate_opposite, FunctionInputParams
    from restack_google_gemini.task_queue import gemini_task_queue

class WorkflowInputParams(BaseModel):
    user_content: str

@workflow.defn(name="GeminiGenerateOppositeWorkflow")
class GeminiGenerateOppositeWorkflow:
    @workflow.run
    async def run(self, input: WorkflowInputParams):
        return await workflow.step(gemini_generate_opposite, FunctionInputParams(user_content=input.user_content), task_queue=gemini_task_queue, start_to_close_timeout=timedelta(seconds=120))
