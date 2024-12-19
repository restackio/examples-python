from restack_ai.workflow import workflow, workflow_import
from typing import Any
from dataclasses import dataclass
from datetime import timedelta

with workflow_import():
    from src.functions.make_changes import make_changes, FunctionInputParams as MakeChangesFunctionInputParams
    from src.functions.generate_pr_info import generate_pr_info, FunctionInputParams as GeneratePrInfoFunctionInputParams
@dataclass
class WorkflowInputParams:
    files_to_create_or_update: list[Any]
    repo_path: str
    chat_history: list[Any]
    user_content: str | None = None

@workflow.defn(name="MakeChangesWorkflow")
class MakeChangesWorkflow:
    @workflow.run
    async def run(self, input: WorkflowInputParams):

        if input.user_content is None:
            await workflow.step(
                make_changes, 
                MakeChangesFunctionInputParams(files_to_create_or_update=input.files_to_create_or_update), 
                start_to_close_timeout=timedelta(seconds=10)
            )

        return await workflow.step(
            generate_pr_info, 
            GeneratePrInfoFunctionInputParams(
                user_content=input.user_content,
                chat_history=input.chat_history,
                repo_path=input.repo_path
            ), 
            start_to_close_timeout=timedelta(seconds=10)
        )