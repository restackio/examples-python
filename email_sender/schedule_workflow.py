import asyncio
import time
from restack_ai import Restack
from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class InputParams:
    email_context: str
    subject: str
    to: str

async def main():
    client = Restack()

    workflow_id = f"{int(time.time() * 1000)}-SendEmailWorkflow"
    to_email = os.getenv("TO_EMAIL")
    if not to_email:
        raise Exception("TO_EMAIL environment variable is not set")

    run_id = await client.schedule_workflow(
        workflow_name="SendEmailWorkflow",
        workflow_id=workflow_id,
        input={
            "email_context": "This email should contain a greeting. And telling user we have launched a new AI feature with Restack workflows. Workflows now offer logging and automatic retries when one of its steps fails. Name of user is not provided. You can set as goodbye message on the email just say 'Best regards' or something like that. No need to mention name of user or name of person sending the email.",
            "subject": "Hello from Restack",
            "to": to_email
        }
    )

    await client.get_workflow_result(
        workflow_id=workflow_id,
        run_id=run_id
    )

    exit(0)

def run_schedule_workflow():
    asyncio.run(main())

if __name__ == "__main__":
    run_schedule_workflow()
