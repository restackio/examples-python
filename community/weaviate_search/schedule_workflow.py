import asyncio
import sys
import time

from restack_ai import Restack


async def schedule_workflow(workflow_name: str) -> None:
    client = Restack()

    workflow_id = f"{int(time.time() * 1000)}-{workflow_name}"
    run_id = await client.schedule_workflow(
        workflow_name=workflow_name,
        workflow_id=workflow_id,
    )

    await client.get_workflow_result(
        workflow_id=workflow_id,
        run_id=run_id,
    )

    sys.exit(0)


def run_schedule_seed_workflow() -> None:
    asyncio.run(schedule_workflow("SeedWorkflow"))


def run_schedule_search_workflow() -> None:
    asyncio.run(schedule_workflow("SearchWorkflow"))


if __name__ == "__main__":
    run_schedule_seed_workflow()
