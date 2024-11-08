from restack_ai.workflow import workflow, import_functions
from restack_ai import log
from dataclasses import dataclass
from datetime import timedelta

with import_functions():
    from src.functions.function import gemini_generate_opposite, FunctionInputParams

@dataclass
class WorkflowInputParams:
    user_content: str

@workflow.defn(name="GeminiGenerateOppositeWorkflow")
class GeminiGenerateOppositeWorkflow:
    @workflow.run
    async def run(self, input: WorkflowInputParams):
        result = await workflow.step(
            gemini_generate_opposite,
            FunctionInputParams(user_content=input.user_content),
            start_to_close_timeout=timedelta(seconds=120)
        )
        log.info("Workflow result", result=result)
        return result
