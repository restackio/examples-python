import asyncio
import time
from restack_ai import Restack
from dotenv import load_dotenv

load_dotenv()

async def main():
    client = Restack()

    workflow_id = f"{int(time.time() * 1000)}-CreatePaymentLinkWorkflow"

    run_id = await client.schedule_workflow(
        workflow_name="CreatePaymentLinkWorkflow",
        workflow_id=workflow_id,
    )

    result = await client.get_workflow_result(
        workflow_id=workflow_id,
        run_id=run_id
    )

    print(result)

    exit(0)

def run_schedule_workflow():
    asyncio.run(main())

if __name__ == "__main__":
    run_schedule_workflow()