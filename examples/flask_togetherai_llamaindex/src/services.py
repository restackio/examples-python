import asyncio
from src.functions.llm_complete import llm_complete
from src.client import restack_client
from src.workflows.workflow import llm_complete_workflow
from dotenv import load_dotenv
load_dotenv()

async def main():
    await restack_client.start_service(
        workflows= [llm_complete_workflow],
        functions= [llm_complete]
    )

def run_services():
    asyncio.run(main())

if __name__ == "__main__":
    run_services()