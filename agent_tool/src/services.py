import asyncio
import os
from watchfiles import run_process
import webbrowser
from src.client import client
from src.functions.lookup_sales import lookupSales
from src.functions.llm_chat import llm_chat

from src.agents.chat_tool_functions import AgentChatToolFunctions
# Step 5: Import a new function to tool calling here
# from src.functions.new_function import new_function, FunctionInput, FunctionOutput

async def main():

    await client.start_service(
        agents=[AgentChatToolFunctions],
        ## Step 6: Add your new function to the functions list -> functions=[lookupSales, llm_chat, new_function]
        functions=[lookupSales, llm_chat]
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
