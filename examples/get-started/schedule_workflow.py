import asyncio
import time
from src.client import client

async def schedule_workflow():
    workflow_id = f"{int(time.time() * 1000)}-greeting_workflow"
    runId = await client.schedule_workflow(
        workflow_name="greeting_workflow",
        workflow_id=workflow_id
    )

    result = await client.get_workflow_status(
        workflow_id=workflow_id,
        run_id=runId
    )
    print(result)

    exit(0)

if __name__ == "__main__":
    asyncio.run(schedule_workflow())