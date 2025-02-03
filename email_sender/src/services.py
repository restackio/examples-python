import asyncio

from src.client import client
from src.functions.generate_email_content import generate_email_content
from src.functions.send_email import send_email
from src.workflows.send_email import SendEmailWorkflow


async def main():
    await asyncio.gather(
        client.start_service(
            workflows=[SendEmailWorkflow],
            functions=[generate_email_content, send_email],
        ),
    )

def run_services():
    asyncio.run(main())

if __name__ == "__main__":
    run_services()
