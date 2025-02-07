import asyncio
import logging
import webbrowser
from pathlib import Path

from restack_ai.restack import ServiceOptions
from watchfiles import run_process

from src.client import client
from src.functions.function import example_function
from src.functions.list_voices import lmnt_list_voices
from src.functions.synthesize import lmnt_synthesize
from src.workflows.workflow import ChildWorkflow, ExampleWorkflow


async def main() -> None:
    await asyncio.gather(
        client.start_service(
            workflows=[ExampleWorkflow, ChildWorkflow],
            functions=[example_function],
            options=ServiceOptions(
                max_concurrent_workflow_runs=1000,
            ),
        ),
        client.start_service(
            task_queue="lmnt",
            functions=[lmnt_synthesize, lmnt_list_voices],
            options=ServiceOptions(
                rate_limit=2,
                max_concurrent_function_runs=4,
            ),
        ),
    )


def run_services() -> None:
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Service interrupted by user. Exiting gracefully.")


def watch_services() -> None:
    watch_path = Path.cwd()
    logging.info("Watching %s and its subdirectories for changes...", watch_path)
    webbrowser.open("http://localhost:5233")
    run_process(watch_path, recursive=True, target=run_services)


if __name__ == "__main__":
    run_services()
