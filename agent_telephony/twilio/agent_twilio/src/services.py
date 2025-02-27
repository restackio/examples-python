import asyncio
import logging
import webbrowser
from pathlib import Path

from watchfiles import run_process

from src.agents.agent import AgentTwilio
from src.client import client
from src.functions.livekit_call import livekit_call
from src.functions.livekit_dispatch import livekit_dispatch
from src.functions.livekit_outbound_trunk import livekit_outbound_trunk
from src.functions.livekit_room import livekit_room
from src.functions.llm_chat import llm_chat


async def main() -> None:
    await client.start_service(
        agents=[AgentTwilio],
        functions=[
            llm_chat,
            livekit_dispatch,
            livekit_call,
            livekit_room,
            livekit_outbound_trunk,
        ],
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
