import asyncio
import logging
import webbrowser
from pathlib import Path

from src.client import client
from src.functions.decide import decide
from src.functions.generate_email_content import generate_email_content
from src.functions.send_email import send_email
from src.workflows.child_workflow_a import ChildWorkflowA
from src.workflows.child_workflow_b import ChildWorkflowB
from src.workflows.parent_workflow import ParentWorkflow
from watchfiles import run_process


async def main() -> None:
    await asyncio.gather(
        client.start_service(
            workflows=[ParentWorkflow, ChildWorkflowA, ChildWorkflowB],
            functions=[decide, generate_email_content, send_email],
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
