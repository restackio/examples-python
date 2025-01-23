from restack_ai.workflow import workflow, import_functions, log, RetryPolicy
from pydantic import BaseModel
from datetime import timedelta

with import_functions():
    from src.functions.generate_content import gemini_generate_content, FunctionInputParams

class WorkflowInputParams(BaseModel):
    user_content: str = "what's the weather in San Francisco?"

@workflow.defn()
class GeminiGenerateContentWorkflow:
    @workflow.run
    async def run(self, input: WorkflowInputParams):
        log.info("GeminiGenerateContentWorkflow started", input=input)
        result = await workflow.step(
            gemini_generate_content,
            FunctionInputParams(user_content=input.user_content),
            start_to_close_timeout=timedelta(seconds=120),
            retry_policy=RetryPolicy(
                maximum_attempts=1
            ),
            task_queue="gemini"
        )
        log.info("GeminiGenerateContentWorkflow completed", result=result)
        return result
