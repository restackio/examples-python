import asyncio
import time
from restack_ai import Restack
from restack_ai.restack import ScheduleSpec, ScheduleIntervalSpec
from datetime import timedelta
from src.workflows.workflow import GreetingWorkflowInput
async def main():

    client = Restack()

    workflow_id = f"{int(time.time() * 1000)}-GreetingWorkflow"
    await client.schedule_workflow(
        workflow_name="GreetingWorkflow",
        workflow_id=workflow_id,
        input=GreetingWorkflowInput(name="Bob"),
        schedule=ScheduleSpec(
            intervals=[ScheduleIntervalSpec(
                every=timedelta(minutes=10)
            )]
        )
    )

    exit(0)

def run_schedule_interval():
    asyncio.run(main())

if __name__ == "__main__":
    run_schedule_interval()