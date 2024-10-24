import asyncio
from src.functions.function import welcome
from src.functions.query import query
from src.client import restack_client
from src.workflows.workflow import GreetingWorkflow, QueryWorkflow

async def main():

    await restack_client.start_service({
        "workflows": [GreetingWorkflow, QueryWorkflow],
        "functions": [welcome, query]
    })

def run_services():
    asyncio.run(main())

if __name__ == "__main__":
    run_services()