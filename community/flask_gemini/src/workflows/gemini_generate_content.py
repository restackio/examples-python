from dataclasses import dataclass
from datetime import timedelta

from restack_ai.workflow import import_functions, log, workflow

with import_functions():
    from src.functions.function import FunctionInputParams, gemini_generate


@dataclass
class WorkflowInputParams:
    user_content: str


@workflow.defn()
class GeminiGenerateWorkflow:
    @workflow.run
    async def run(self, input: WorkflowInputParams):
        log.info("GeminiGenerateWorkflow started", input=input)
        result = await workflow.step(
            gemini_generate,
            FunctionInputParams(user_content=input.user_content),
            start_to_close_timeout=timedelta(seconds=120),
        )
        log.info("GeminiGenerateWorkflow completed", result=result)
        return result
