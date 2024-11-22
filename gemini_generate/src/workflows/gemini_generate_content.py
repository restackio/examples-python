from restack_ai.workflow import workflow, import_functions, log
from dataclasses import dataclass
from datetime import timedelta

with import_functions():
    from src.functions.function import gemini_generate_opposite, FunctionInputParams

@dataclass
class WorkflowInputParams:
    user_content: str

@workflow.defn()
class GeminiGenerateOppositeWorkflow:
    @workflow.run
    async def run(self, input: WorkflowInputParams):
        log.info("GeminiGenerateOppositeWorkflow started", input=input)
        result = await workflow.step(
            gemini_generate_opposite,
            FunctionInputParams(user_content=input.user_content),
            start_to_close_timeout=timedelta(seconds=120)
        )
        log.info("GeminiGenerateOppositeWorkflow completed", result=result)
        return result
