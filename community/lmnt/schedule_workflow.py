import asyncio
import sys
import time

from src.client import client
from src.workflows.child import ChildWorkflowInput


async def main() -> None:
    workflow_id = f"{int(time.time() * 1000)}-ChildWorkflow"
    run_id = await client.schedule_workflow(
        workflow_name="ChildWorkflow",
        workflow_id=workflow_id,
        input=ChildWorkflowInput(name="Hi, my name is John Doe", voice="morgan"),
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
