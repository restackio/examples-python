import asyncio
from src.functions.llm_complete import llm_complete
from src.client import restack_client
from src.workflows.workflow import LlmCompleteWorkflow
from dotenv import load_dotenv
load_dotenv()

async def main():
    await restack_client.start_service(
        workflows= [LlmCompleteWorkflow],
        functions= [llm_complete]
    )

def run_services():
    asyncio.run(main())

if __name__ == "__main__":
    run_services()