import asyncio
import logging
from pathlib import Path

from watchfiles import run_process

from src.client import client
from src.functions.function import isolate_audio, text_to_speech
from src.workflows.workflow import AudioIsolationWorkflow, TextToSpeechWorkflow


async def main() -> None:
    await client.start_service(
        workflows=[TextToSpeechWorkflow, AudioIsolationWorkflow],
        functions=[text_to_speech, isolate_audio],
    )


def run_services() -> None:
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Service interrupted by user. Exiting gracefully.")


def watch_services() -> None:
    watch_path = Path.cwd()
    logging.info("Watching %s and its subdirectories for changes...", watch_path)
    run_process(watch_path, recursive=True, target=run_services)
