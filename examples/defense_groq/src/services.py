import asyncio
from src.client import client
from src.functions.transcribe import transcribe
from src.workflows.transcribe import TranscribeWorkflow
from restack_ai.restack import ServiceOptions

async def main():
    await asyncio.gather(
        client.start_service(
            workflows=[TranscribeWorkflow],
            functions=[transcribe]
        ),
        client.start_service(
            functions=[transcribe],
            task_queue="transcribe",
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
