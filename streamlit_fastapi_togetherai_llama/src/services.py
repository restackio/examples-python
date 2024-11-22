import asyncio
from src.client import client
from src.functions.function import llm_complete
from src.workflows.workflow import LlmCompleteWorkflow

async def main():
    await client.start_service(
        workflows= [LlmCompleteWorkflow],
        functions= [llm_complete]
    )

def run_services():
    asyncio.run(main())

if __name__ == "__main__":
    run_services()
