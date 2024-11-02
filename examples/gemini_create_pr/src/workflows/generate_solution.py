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
        generate_solution_response = None

        print(f"Input history: {input.chat_history}")

        if len(input.chat_history) == 0:
            scan_repository_response = await workflow.step(
                scan_repository, 
                ScanRepositoryFunctionInputParams(repo_path=input.repo_path), 
                start_to_close_timeout=timedelta(seconds=10)
            )

            generate_solution_response = await workflow.step(
                generate_solution, 
                GenerateSolutionFunctionInputParams(repo_contents_file_path=scan_repository_response.output_file, user_content=input.user_content, chat_history=input.chat_history), 
                start_to_close_timeout=timedelta(seconds=10)
            )

        if len(input.chat_history) > 0:
            generate_solution_response = await workflow.step(
                generate_solution, 
                GenerateSolutionFunctionInputParams(repo_contents_file_path=None, user_content=input.user_content, chat_history=input.chat_history), 
                start_to_close_timeout=timedelta(seconds=10)
            )

        print(f"Generate solution response: {generate_solution_response.chat_history}")

        return generate_solution_response