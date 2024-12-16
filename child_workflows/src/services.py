import asyncio
import os
from watchfiles import run_process
from restack_ai.restack import ServiceOptions
from src.functions.function import welcome
from src.client import client
from src.workflows.parent import ParentWorkflow
from src.workflows.child import ChildWorkflow

async def main():
    await client.start_service(
        workflows= [ParentWorkflow, ChildWorkflow],
        functions= [welcome],
        options=ServiceOptions(
            endpoints= True
        ),
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