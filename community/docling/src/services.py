import asyncio

from src.agents.agent import Agent
from src.client import client
from src.functions.function import (
    welcome,
)
from src.workflows.workflow import (
    Workflow,
)

async def main():

    await client.start_service(
        agents=[
            Agent,
        ],
        workflows=[
            Workflow,
        ],
        functions=[
            welcome,
        ]
    )


def run_services():
    asyncio.run(main())


if __name__ == "__main__":
    run_services()