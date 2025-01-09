from restack_ai.workflow import workflow, workflow_import
from dataclasses import dataclass
from datetime import timedelta

with workflow_import():
    from src.functions.create_pr import create_pr, FunctionInputParams as CreatePrFunctionInputParams
    from src.functions.generate_pr_info import PrInfo


@dataclass
class WorkflowInputParams:
    repo_path: str
    pr_info: PrInfo

@workflow.defn(name="CreatePrWorkflow")
class CreatePrWorkflow:
    @workflow.run
    async def run(self, input: WorkflowInputParams):
        result = await workflow.step(
            create_pr, 
            CreatePrFunctionInputParams(
                repo_path=input.repo_path,
                pr_info=input.pr_info
            ), 
            start_to_close_timeout=timedelta(seconds=10)
        )
        return result