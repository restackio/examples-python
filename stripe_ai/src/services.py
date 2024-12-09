import asyncio
from src.client import client
from src.workflows.payment_link import CreatePaymentLinkWorkflow
from src.functions.create_payment_link import create_payment_link

async def main():
    await asyncio.gather(
        client.start_service(
            workflows=[CreatePaymentLinkWorkflow],
            functions=[create_payment_link]
        )
    )

def run_services():
    asyncio.run(main())

if __name__ == "__main__":
    run_services()
