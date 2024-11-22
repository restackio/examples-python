import asyncio
from src.functions.seed_database import seed_database
from src.functions.vector_search import vector_search
from src.client import restack_client
from src.workflows.workflow import SeedWorkflow, SearchWorkflow
from dotenv import load_dotenv
load_dotenv()

async def main():
    await restack_client.start_service(
        workflows= [SeedWorkflow, SearchWorkflow],
        functions= [seed_database, vector_search]
    )

def run_services():
    asyncio.run(main())

if __name__ == "__main__":
    run_services()