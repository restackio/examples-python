import asyncio
from src.client import client
from src.functions.function import llm_complete
from src.workflows.workflow import LlmCompleteWorkflow
from restack_ai.restack import ServiceOptions

async def main():
    await asyncio.gather(
        client.start_service(
            workflows=[LlmCompleteWorkflow],
            functions=[llm_complete],
            options=ServiceOptions(
                rate_limit=1,
                max_concurrent_function_runs=1
            )
        )
    )

def run_services():
    asyncio.run(main())

if __name__ == "__main__":
    run_services()