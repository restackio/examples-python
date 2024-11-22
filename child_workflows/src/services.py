import asyncio
from src.functions.function import welcome
from src.client import client
from src.workflows.parent import ParentWorkflow
from src.workflows.child import ChildWorkflow

async def main():

    await client.start_service(
        workflows= [ParentWorkflow, ChildWorkflow],
        functions= [welcome]
    )

def run_services():
    asyncio.run(main())

if __name__ == "__main__":
    run_services()