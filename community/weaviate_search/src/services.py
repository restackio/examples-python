import asyncio

from dotenv import load_dotenv

from src.client import restack_client
from src.functions.seed_database import seed_database
from src.functions.vector_search import vector_search
from src.workflows.workflow import SearchWorkflow, SeedWorkflow

load_dotenv()


async def main():
    await restack_client.start_service(
        workflows=[SeedWorkflow, SearchWorkflow],
        functions=[seed_database, vector_search],
    )


def run_services():
    asyncio.run(main())


if __name__ == "__main__":
    run_services()
