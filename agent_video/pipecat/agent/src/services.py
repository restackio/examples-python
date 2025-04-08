import asyncio
import logging
import webbrowser
from pathlib import Path

from restack_ai.restack import ServiceOptions
from watchfiles import run_process

from src.agents.agent import AgentVideo
from src.client import client
from src.functions.context_docs import context_docs
from src.functions.daily_create_room import daily_create_room
from src.functions.daily_send_data import daily_send_data
from src.functions.llm_logic import llm_logic
from src.functions.llm_talk import llm_talk
from src.functions.send_agent_event import send_agent_event
from src.functions.tavus_create_room import tavus_create_room
from src.workflows.logic import LogicWorkflow
from src.workflows.room import RoomWorkflow


async def main() -> None:
    await client.start_service(
        agents=[AgentVideo],
        workflows=[RoomWorkflow, LogicWorkflow],
        functions=[
            llm_logic,
            llm_talk,
            context_docs,
            daily_create_room,
            tavus_create_room,
            daily_send_data,
            send_agent_event,
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
