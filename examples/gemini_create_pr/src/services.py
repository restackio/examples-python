import asyncio
from src.client import client

from src.functions import scan_repository, generate_solution, make_changes, generate_pr_info, create_pr
from src.workflows import GenerateSolutionWorkflow, MakeChangesWorkflow, CreatePrWorkflow


async def main():
    await client.start_service(
        workflows=[GenerateSolutionWorkflow, MakeChangesWorkflow, CreatePrWorkflow],
        functions=[scan_repository, generate_solution, make_changes, create_pr, generate_pr_info],
    )

def run_services():
    asyncio.run(main())

if __name__ == "__main__":
    run_services()