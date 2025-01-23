import asyncio
from src.client import client
from src.functions.decide import decide
from src.functions.generate_email_content import generate_email_content
from src.functions.send_email import send_email
from src.workflows.parent_workflow import ParentWorkflow
from src.workflows.child_workflow_a import ChildWorkflowA
from src.workflows.child_workflow_b import ChildWorkflowB

async def main():
    await asyncio.gather(
        client.start_service(
            workflows=[ParentWorkflow, ChildWorkflowA, ChildWorkflowB],
            functions=[decide, generate_email_content, send_email]
        )
    )

def run_services():
    asyncio.run(main())

if __name__ == "__main__":
    run_services()
