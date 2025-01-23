import asyncio
import time
from restack_ai import Restack

async def main():

    client = Restack()

    workflow_id = f"{int(time.time() * 1000)}-ParentWorkflow"
    runId = await client.schedule_workflow(
        workflow_name="ParentWorkflow",
        workflow_id=workflow_id,
        input={
            "email": "admin@example.com",
            "current_accepted_applicants_count": 10
        }
    )

    await client.get_workflow_result(
        workflow_id=workflow_id,
        run_id=runId
    )

    exit(0)

def run_schedule_workflow():
    asyncio.run(main())

if __name__ == "__main__":
    run_schedule_workflow()