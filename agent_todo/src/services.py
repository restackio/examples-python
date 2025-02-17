import asyncio
import logging
import webbrowser
from pathlib import Path

from watchfiles import run_process

from src.agents.agent_todo import AgentTodo
from src.client import client
from src.functions.get_random import get_random
from src.functions.get_result import get_result
from src.functions.llm_chat import llm_chat
from src.functions.todo_create import todo_create
from src.workflows.todo_execute import TodoExecute


async def main() -> None:
    await client.start_service(
        agents=[AgentTodo],
        workflows=[TodoExecute],
        functions=[todo_create, get_random, get_result, llm_chat],
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
