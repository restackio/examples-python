import os
import asyncio
from src.client import client
from watchfiles import run_process
# import webbrowser

## Workflow and function imports
from src.workflows.send_email import SendEmailWorkflow
from src.functions.smtp_send_email import smtp_send_email

async def main():
    await asyncio.gather(
        client.start_service(
            workflows=[SendEmailWorkflow],
            functions=[smtp_send_email]
        )
    )

def run_services():
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Service interrupted by user. Exiting gracefully.")

def watch_services():
    watch_path = os.getcwd()
    print(f"Watching {watch_path} and its subdirectories for changes...")
    # Opens default browser to Dev UI
    # webbrowser.open("http://localhost:5233")
    run_process(watch_path, recursive=True, target=run_services)

if __name__ == "__main__":
    run_services()
