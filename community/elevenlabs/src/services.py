import asyncio
import os

from watchfiles import run_process

from src.client import client
from src.functions.function import isolate_audio, text_to_speech
from src.workflows.workflow import AudioIsolationWorkflow, TextToSpeechWorkflow


async def main():
    await client.start_service(
        workflows=[TextToSpeechWorkflow, AudioIsolationWorkflow],
        functions=[text_to_speech, isolate_audio],
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
