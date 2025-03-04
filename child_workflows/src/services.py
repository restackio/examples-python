import asyncio
import os
import webbrowser

from watchfiles import run_process

from src.client import client
from src.functions.function import welcome
from src.workflows.child import ChildWorkflow
from src.workflows.parent import ParentWorkflow


async def main():
    await client.start_service(
        workflows= [ParentWorkflow, ChildWorkflow],
        functions= [welcome]
    )

def run_services():
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Service interrupted by user. Exiting gracefully.")


def watch_services():
    watch_path = os.getcwd()
    print(f"Watching {watch_path} and its subdirectories for changes...")
    webbrowser.open("http://localhost:5233")
    run_process(watch_path, recursive=True, target=run_services)

if __name__ == "__main__":
       run_services()
