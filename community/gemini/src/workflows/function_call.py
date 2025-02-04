from datetime import timedelta

from pydantic import BaseModel
from restack_ai.workflow import RetryPolicy, import_functions, log, workflow

with import_functions():
    from src.functions.function_call import FunctionInputParams, gemini_function_call


class WorkflowInputParams(BaseModel):
    user_content: str = "what's the weather in San Francisco?"


@workflow.defn()
class GeminiFunctionCallWorkflow:
    @workflow.run
    async def run(self, input: WorkflowInputParams):
        log.info("GeminiFunctionCallWorkflow started", input=input)
        result = await workflow.step(
            gemini_function_call,
            FunctionInputParams(user_content=input.user_content),
            start_to_close_timeout=timedelta(seconds=120),
            retry_policy=RetryPolicy(
                maximum_attempts=1,
            ),
            task_queue="gemini",
        )
        log.info("GeminiFunctionCallWorkflow completed", result=result)
        return result
