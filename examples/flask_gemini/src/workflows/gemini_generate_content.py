from restack_ai.workflow import workflow, import_functions, log
from pydantic import BaseModel
from datetime import timedelta

with import_functions():
    from src.functions.function import gemini_generate, FunctionInputParams

class WorkflowInputParams(BaseModel):
    user_content: str

@workflow.defn(name="GeminiGenerateWorkflow")
class GeminiGenerateWorkflow:
    @workflow.run
    async def run(self, input: WorkflowInputParams):
        log.info(input)
        return await workflow.step(gemini_generate, FunctionInputParams(user_content=input.user_content), start_to_close_timeout=timedelta(seconds=120))
