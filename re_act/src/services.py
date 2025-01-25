import asyncio
import os
from src.client import client
from src.functions.decide import decide
from src.functions.generate_email_content import generate_email_content
from src.functions.send_email import send_email
from src.workflows.parent_workflow import ParentWorkflow
from src.workflows.child_workflow_a import ChildWorkflowA
from src.workflows.child_workflow_b import ChildWorkflowB
from watchfiles import run_process
import webbrowser

async def main():
    await asyncio.gather(
        client.start_service(
            workflows=[ParentWorkflow, ChildWorkflowA, ChildWorkflowB],
            functions=[decide, generate_email_content, send_email]
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
    webbrowser.open("http://localhost:5233")
    run_process(watch_path, recursive=True, target=run_services)

if __name__ == "__main__":
       run_services()
