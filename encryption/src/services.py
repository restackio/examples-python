import asyncio

from src.client import client
from src.functions.function import welcome
from src.workflows.workflow import EncryptedWorkflow


async def main() -> None:
    await client.start_service(
        workflows=[EncryptedWorkflow],
        functions=[welcome],
    )


def run_services() -> None:
    asyncio.run(main())


if __name__ == "__main__":
    run_services()
