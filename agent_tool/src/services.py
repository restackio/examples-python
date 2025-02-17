# ruff: noqa: ERA001
import asyncio
import logging
import webbrowser
from pathlib import Path

from watchfiles import run_process

from src.agents.chat_tool_functions import AgentChatToolFunctions
from src.client import client
from src.functions.llm_chat import llm_chat
from src.functions.lookup_sales import lookup_sales

# Step 5: Import a new function to tool calling here
# from src.functions.new_function import new_function, FunctionInput, FunctionOutput


async def main() -> None:
    await client.start_service(
        agents=[AgentChatToolFunctions],
        ## Step 6: Add your new function to the functions list -> functions=[lookupSales, llm_chat, new_function]
        functions=[lookup_sales, llm_chat],
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
