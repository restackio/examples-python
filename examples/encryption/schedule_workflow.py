import asyncio
import time
from src.client import client
async def main():

    workflow_id = f"{int(time.time() * 1000)}-EncryptedWorkflow"
    run_id = await client.schedule_workflow(
        workflow_name="EncryptedWorkflow",
        workflow_id=workflow_id
    )

    await client.get_workflow_result(
        workflow_id=workflow_id,
        run_id=run_id
    )

    exit(0)

def run_schedule_workflow():
    asyncio.run(main())

if __name__ == "__main__":
    run_schedule_workflow()