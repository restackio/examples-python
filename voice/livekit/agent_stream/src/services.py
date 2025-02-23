import asyncio
import os
from src.functions.llm_chat import llm_chat
from src.client import client
from src.agents.agent import AgentStream
from src.functions.livekit_dispatch import livekit_dispatch
from src.functions.livekit_token import livekit_token
from src.functions.livekit_call import livekit_call
from src.functions.livekit_room import livekit_room
from src.functions.livekit_outbound_trunk import livekit_outbound_trunk

from watchfiles import run_process
import webbrowser

async def main():

    await client.start_service(
        agents=[AgentStream],
        functions=[llm_chat, livekit_dispatch, livekit_token, livekit_call, livekit_room, livekit_outbound_trunk]
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
