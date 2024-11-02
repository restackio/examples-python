import asyncio
from src.client import client
from src.functions.repo_contents import scan_repository
from src.functions.generate_solution import generate_solution
from src.functions.make_changes import make_changes
from src.functions.generate_pr_info import generate_pr_info
from src.functions.create_pr import create_pr
from src.workflows.generate_solution import GenerateSolutionWorkflow
from src.workflows.make_changes import MakeChangesWorkflow
from src.workflows.create_pr import CreatePrWorkflow

async def main():
    await client.start_service(
        workflows=[GenerateSolutionWorkflow, MakeChangesWorkflow, CreatePrWorkflow],
        functions=[scan_repository, generate_solution, make_changes, create_pr, generate_pr_info],
    )

def run_services():
    asyncio.run(main())

if __name__ == "__main__":
    run_services()