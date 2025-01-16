import asyncio
from src.client import client
from src.workflows.workflow import SpotWorkflow
async def main():

    await client.start_service(
        workflows= [SpotWorkflow]
    )

def run_services():
    asyncio.run(main())

if __name__ == "__main__":
    run_services()