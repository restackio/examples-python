import asyncio
import sys
import time

from restack_ai import Restack


async def main() -> None:
    client = Restack()

    workflow_id = f"{int(time.time() * 1000)}-ChildWorkflow"
    run_id = await client.schedule_workflow(
        workflow_name="ChildWorkflow",
        workflow_id=workflow_id,
    )

    await client.get_workflow_result(
        workflow_id=workflow_id,
        run_id=run_id,
    )

    sys.exit(0)


def run_schedule_workflow() -> None:
    asyncio.run(main())


if __name__ == "__main__":
    run_schedule_workflow()
