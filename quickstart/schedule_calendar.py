import asyncio
import time
from restack_ai import Restack
from restack_ai.restack import ScheduleSpec, ScheduleCalendarSpec, ScheduleRange
from src.workflows.workflow import GreetingWorkflowInput
async def main():

    client = Restack()

    workflow_id = f"{int(time.time() * 1000)}-GreetingWorkflow"
    await client.schedule_workflow(
        workflow_name="GreetingWorkflow",
        workflow_id=workflow_id,
        input=GreetingWorkflowInput(name="Bob"),
        schedule=ScheduleSpec(
            calendars=[ScheduleCalendarSpec(
                day_of_week=[ScheduleRange(start=1)],
                hour=[ScheduleRange(start=9)]
            )]
        )
    )

    exit(0)

def run_schedule_calendar():
    asyncio.run(main())

if __name__ == "__main__":
    run_schedule_calendar()