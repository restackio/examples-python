import asyncio

from dotenv import load_dotenv

from src.client import restack_client
from src.functions.llm_complete import llm_complete
from src.workflows.workflow import LlmCompleteWorkflow

load_dotenv()

async def main():
    await restack_client.start_service(
        workflows= [LlmCompleteWorkflow],
        functions= [llm_complete],
    )

def run_services():
    asyncio.run(main())

if __name__ == "__main__":
    run_services()
