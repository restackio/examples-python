import asyncio
from watchfiles import run_process
import webbrowser
import os

from src.client import client
from src.functions.function import gemini_generate_opposite
from src.workflows.gemini_generate_content import GeminiGenerateOppositeWorkflow
async def main():
    await client.start_service(
        workflows= [GeminiGenerateOppositeWorkflow],
        functions= [gemini_generate_opposite]
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