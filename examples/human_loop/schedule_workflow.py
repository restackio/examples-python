import asyncio
import time
from restack_ai import Restack, log

async def main():

    client = Restack()

    workflow_id = f"{int(time.time() * 1000)}-HumanLoopWorkflow"
    runId = await client.schedule_workflow(
        workflow_name="HumanLoopWorkflow",
        workflow_id=workflow_id
    )

    feedback = await client.send_workflow_event(
        event_name="event_feedback",
        event_input={
            "feedback": "This is a human feedback"
        },
        workflow_id=workflow_id,
        run_id=runId,
    )

    log.info("Feedback sent", feedback=feedback)

    end = await client.send_workflow_event(
        event_name="event_end",
        event_input={
            "end": True
        },
        workflow_id=workflow_id,
        run_id=runId,
    )

    log.info("Workflow ended", end=end)

    exit(0)

def run_schedule_workflow():
    asyncio.run(main())

if __name__ == "__main__":
    run_schedule_workflow()