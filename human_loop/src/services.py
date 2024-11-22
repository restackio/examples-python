import asyncio
from src.functions.function import feedback, goodbye
from src.client import client
from src.workflows.workflow import HumanLoopWorkflow

async def main():

    await client.start_service(
        workflows= [HumanLoopWorkflow],
        functions= [feedback, goodbye]
    )

def run_services():
    asyncio.run(main())

if __name__ == "__main__":
    run_services()