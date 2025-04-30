import asyncio
import os
from watchfiles import run_process
import webbrowser

from src.client import client
from restack_ai.restack import ServiceOptions

from src.functions.create_meet_bot import create_meet_bot
from src.functions.get_bot_transcript import get_bot_transcript
from src.functions.retrieve_bot import retrieve_bot
from src.workflows.create_meet_bot import CreateMeetBotWorkflow
from src.workflows.summarize_meeting import SummarizeMeetingWorkflow
from src.functions.list_bots import list_bots
from src.functions.summarize_transcript import summarize_transcript

async def main():

    await asyncio.gather(
        client.start_service(
            functions=[create_meet_bot, get_bot_transcript, retrieve_bot, list_bots],
            options=ServiceOptions(
                max_concurrent_workflow_runs=1000
            ),
            task_queue='recall',
        ),
        client.start_service(
            workflows=[SummarizeMeetingWorkflow, CreateMeetBotWorkflow],
        ),
        client.start_service(
            functions=[summarize_transcript],
            task_queue='gemini',
            options=ServiceOptions(
                rate_limit=1,
                max_concurrent_function_runs=5
            ),
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
    webbrowser.open("http://localhost:5233")
    run_process(watch_path, recursive=True, target=run_services)

if __name__ == "__main__":
    run_services()