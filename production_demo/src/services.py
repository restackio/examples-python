import asyncio
import os
from src.functions.function import example_function
from src.functions.openai import openai_joke
from src.client import client
from src.workflows.workflow import ExampleWorkflow, ChildWorkflow
from watchfiles import run_process
from restack_ai.restack import ServiceOptions
async def main():

    await asyncio.gather(
        client.start_service(
            workflows=[ExampleWorkflow, ChildWorkflow],
            functions=[example_function],
            options=ServiceOptions(
                max_concurrent_workflow_runs=1000
            )

        ),
        client.start_service(
            task_queue="openai",
            functions=[openai_joke],
            options=ServiceOptions(
                rate_limit=1,
                max_concurrent_function_runs=1
            )
        )
    )

def run_services():
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Service interrupted by user. Exiting gracefully.")

def watch_services():
    watch_path = os.getcwd()
    print(f"Watching {watch_path} and its subdirectories for changes...")
    run_process(watch_path, recursive=True, target=run_services)

