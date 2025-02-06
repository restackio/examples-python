import asyncio
import logging
import sys
import time

from dotenv import load_dotenv
from restack_ai import Restack

load_dotenv()


async def main() -> None:
    client = Restack()

    workflow_id = f"{int(time.time() * 1000)}-CreatePaymentLinkWorkflow"

    run_id = await client.schedule_workflow(
        workflow_name="CreatePaymentLinkWorkflow",
        workflow_id=workflow_id,
    )

    result = await client.get_workflow_result(
        workflow_id=workflow_id,
        run_id=run_id,
    )

    logging.info("Workflow result: %s", result)

    sys.exit(0)


def run_schedule_workflow() -> None:
    asyncio.run(main())


if __name__ == "__main__":
    run_schedule_workflow()
