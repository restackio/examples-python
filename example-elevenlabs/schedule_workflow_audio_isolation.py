import asyncio
import time
from restack_ai import Restack

async def main():
    # Initialize the Restack client
    client = Restack()

    # Generate a unique workflow ID
    workflow_id = f"{int(time.time() * 1000)}-AudioIsolationWorkflow"

    # Schedule the workflow
    run_id = await client.schedule_workflow(
        workflow_name="AudioIsolationWorkflow",
        workflow_id=workflow_id
    )

    # Wait for the workflow result
    result = await client.get_workflow_result(
        workflow_id=workflow_id,
        run_id=run_id
    )

    # Log the result
    print(f"Workflow Result: {result}")

    exit(0)

def run_schedule_workflow_audio_isolation():
    asyncio.run(main())

if __name__ == "__main__":
    run_schedule_workflow_audio_isolation()
