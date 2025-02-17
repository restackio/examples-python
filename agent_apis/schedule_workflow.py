import asyncio
import sys
import time
from dataclasses import dataclass

from restack_ai import Restack


@dataclass
class InputParams:
    name: str


async def main() -> None:
    client = Restack()

    workflow_id = f"{int(time.time() * 1000)}-MultistepWorkflow"
    run_id = await client.schedule_workflow(
        workflow_name="MultistepWorkflow",
        workflow_id=workflow_id,
        workflow_input=InputParams(name="Restack AI SDK User"),
    )

    await client.get_workflow_result(workflow_id=workflow_id, run_id=run_id)

    sys.exit(0)


def run_schedule_workflow() -> None:
    asyncio.run(main())


if __name__ == "__main__":
    run_schedule_workflow()
