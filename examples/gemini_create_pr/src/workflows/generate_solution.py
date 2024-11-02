from restack_ai.workflow import workflow, workflow_import
from typing import Any
from dataclasses import dataclass
from datetime import timedelta

with workflow_import():
    from src.functions.repo_contents import scan_repository, FunctionInputParams as ScanRepositoryFunctionInputParams
    from src.functions.generate_solution import generate_solution, FunctionInputParams as GenerateSolutionFunctionInputParams

@dataclass
class WorkflowInputParams:
    repo_path: str
    user_content: str
    chat_history: list[Any]

@workflow.defn(name="GenerateSolutionWorkflow")
class GenerateSolutionWorkflow:
    @workflow.run
    async def run(self, input: WorkflowInputParams):
        repo_contents_file = None
        if len(input.chat_history) == 0:
            scan_result = await workflow.step(
                scan_repository, 
                ScanRepositoryFunctionInputParams(repo_path=input.repo_path), 
                start_to_close_timeout=timedelta(seconds=10)
            )
            repo_contents_file = scan_result.output_file

        solution = await workflow.step(
            generate_solution, 
            GenerateSolutionFunctionInputParams(
                repo_contents_file_path=repo_contents_file,
                user_content=input.user_content,
                chat_history=input.chat_history
            ), 
            start_to_close_timeout=timedelta(seconds=10)
        )

        return solution