from restack_ai.workflow import workflow, import_functions, log, RetryPolicy
from dataclasses import dataclass
from datetime import timedelta

with import_functions():
    from src.functions.function import gemini_generate_content, FunctionInputParams

@dataclass
class WorkflowInputParams:
    user_content: str

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
            )
        )
        log.info("GeminiGenerateContentWorkflow completed", result=result)
        return result
