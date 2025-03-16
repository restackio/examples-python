import asyncio
import logging
import webbrowser
from pathlib import Path

from watchfiles import run_process

from src.client import client
from src.functions.pipeline_heygen import pipecat_pipeline_heygen
from src.functions.pipeline_tavus import pipecat_pipeline_tavus
from src.workflows.pipeline import PipelineWorkflow
from restack_ai.restack import ServiceOptions
from src.functions.daily_delete_room import daily_delete_room
from src.functions.send_agent_event import send_agent_event
async def main() -> None:
    await client.start_service(
        task_queue="pipeline",
        workflows=[PipelineWorkflow],
        functions=[
            pipecat_pipeline_tavus,
            pipecat_pipeline_heygen,
            daily_delete_room,
            send_agent_event,
        ],
        options=ServiceOptions(
            endpoint_group="agent_video",  # used to locally show both agent and pipeline endpoints in UI
        ),
    )


def run_services() -> None:
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info(
            "Service interrupted by user. Exiting gracefully.",
        )


def watch_services() -> None:
    watch_path = Path.cwd()
    logging.info(
        "Watching %s and its subdirectories for changes...",
        watch_path,
    )
    webbrowser.open("http://localhost:5233")
    run_process(watch_path, recursive=True, target=run_services)


if __name__ == "__main__":
    run_services()
