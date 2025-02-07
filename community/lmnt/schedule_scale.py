import asyncio
import sys
import time

from restack_ai import Restack
from src.workflows.workflow import ExampleWorkflowInput


async def main() -> None:
    client = Restack()

    workflow_id = f"{int(time.time() * 1000)}-ExampleWorkflow"
    await client.schedule_workflow(
        workflow_name="ExampleWorkflow",
        workflow_id=workflow_id,
        input=ExampleWorkflowInput(max_amount=50),
    )

    sys.exit(0)


def run_schedule_scale() -> None:
    asyncio.run(main())


if __name__ == "__main__":
    run_schedule_scale()
