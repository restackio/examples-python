import asyncio
import time
from restack_ai import Restack
from restack_ai.restack import ScheduleSpec, ScheduleIntervalSpec
from datetime import timedelta

async def main():

    client = Restack()

    workflow_id = f"{int(time.time() * 1000)}-ChildWorkflow"
    await client.schedule_workflow(
        workflow_name="ChildWorkflow",
        workflow_id=workflow_id,
        schedule=ScheduleSpec(
            intervals=[ScheduleIntervalSpec(
                every=timedelta(seconds=1)
            )]
        )
    )

    exit(0)

def run_schedule_scale():
    asyncio.run(main())

if __name__ == "__main__":
    run_schedule_scale()