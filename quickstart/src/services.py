import asyncio
import os
from src.functions.random import get_random
from src.functions.result import get_result
from src.client import client
from src.workflows.todo_execute import TodoExecute
from src.agents.agent_todo import AgentTodo
from src.functions.todo_create import todo_create
from src.functions.llm_chat import llm_chat
from watchfiles import run_process
import webbrowser

async def main():
    await client.start_service(
        agents=[AgentTodo],
        workflows=[TodoExecute],
        functions=[todo_create, get_random, get_result, llm_chat]
    )

def run_services():
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Service interrupted by user. Exiting gracefully.")

def watch_services():
    watch_path = os.getcwd()
    print(f"Watching {watch_path} and its subdirectories for changes...")
    webbrowser.open("http://localhost:5233")
    run_process(watch_path, recursive=True, target=run_services)

if __name__ == "__main__":
       run_services()
