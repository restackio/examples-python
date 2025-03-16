import asyncio
import logging
import webbrowser
from pathlib import Path

from watchfiles import run_process

from src.agents.agent import AgentVideo
from src.client import client
from src.functions.context_docs import context_docs
from src.functions.llm_chat import llm_chat
from src.workflows.room import RoomWorkflow
from restack_ai.restack import ServiceOptions
from src.functions.daily_create_room import daily_create_room
from src.functions.tavus_create_room import tavus_create_room
from src.functions.daily_send_data import daily_send_data

async def main() -> None:
    await client.start_service(
        agents=[AgentVideo],
        workflows=[RoomWorkflow],
        functions=[
            llm_chat,
            context_docs,
            daily_create_room,
            tavus_create_room,
            daily_send_data,
        ],
        options=ServiceOptions(
            endpoint_group="agent_video",  # used to locally show both agent and pipeline endpoint in UI
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
