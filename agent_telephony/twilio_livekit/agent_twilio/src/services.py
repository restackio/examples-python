import asyncio
import logging
import webbrowser
from pathlib import Path

from watchfiles import run_process

from src.agents.agent import AgentTwilio
from src.client import client
from src.functions.context_docs import context_docs
from src.functions.livekit_call import livekit_call
from src.functions.livekit_create_room import livekit_create_room
from src.functions.livekit_delete_room import livekit_delete_room
from src.functions.livekit_dispatch import livekit_dispatch
from src.functions.livekit_outbound_trunk import (
    livekit_outbound_trunk,
)
from src.functions.livekit_send_data import livekit_send_data
from src.functions.livekit_start_recording import (
    livekit_start_recording,
)
from src.functions.livekit_token import livekit_token
from src.functions.llm_logic import llm_logic
from src.functions.llm_talk import llm_talk
from src.functions.send_agent_event import send_agent_event
from src.workflows.logic import LogicWorkflow


async def main() -> None:
    await client.start_service(
        agents=[AgentTwilio],
        workflows=[LogicWorkflow],
        functions=[
            llm_talk,
            llm_logic,
            livekit_dispatch,
            livekit_call,
            livekit_create_room,
            livekit_delete_room,
            livekit_outbound_trunk,
            livekit_token,
            context_docs,
            livekit_send_data,
            send_agent_event,
            livekit_start_recording,
        ],
    )


def run_services() -> None:
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info(
            "Service interrupted by user. Exiting gracefully."
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
