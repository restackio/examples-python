import asyncio
import logging
import webbrowser
from pathlib import Path

from restack_ai.restack import ServiceOptions
from src.client import client
from src.functions.evaluate import llm_evaluate
from src.functions.function import example_function
from src.functions.generate import llm_generate
from src.workflows.workflow import ChildWorkflow, ExampleWorkflow
from watchfiles import run_process


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
            task_queue="llm",
            functions=[llm_generate, llm_evaluate],
            options=ServiceOptions(
                rate_limit=1,
                max_concurrent_function_runs=1,
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
