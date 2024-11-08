import asyncio
import time
from restack_ai import Restack, log

async def main():

    client = Restack()

    workflow_id = f"{int(time.time() * 1000)}-GreetingWorkflow"
    runId = await client.schedule_workflow(
        workflow_name="GreetingWorkflow",
        workflow_id=workflow_id
    )

    result = await client.get_workflow_result(
        workflow_id=workflow_id,
        run_id=runId
    )

    log.info("Workflow result", result=result)

    exit(0)

def run_schedule_workflow():
    asyncio.run(main())

if __name__ == "__main__":
    run_schedule_workflow()