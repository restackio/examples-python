import asyncio
import os
from src.functions.function import openai_greet
from src.client import client
from src.workflows.openai_greet import OpenaiGreetWorkflow
from watchfiles import run_process
import webbrowser

async def main():

    await client.start_service(
        workflows= [OpenaiGreetWorkflow],
        functions= [openai_greet],
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