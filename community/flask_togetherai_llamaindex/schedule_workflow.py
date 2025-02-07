import asyncio
import logging
import sys
import time

from restack_ai import Restack


async def schedule_workflow(workflow_name: str) -> None:
    client = Restack()

    logging.info(client)

    workflow_id = f"{int(time.time() * 1000)}-{workflow_name}"
    run_id = await client.schedule_workflow(
        workflow_name=workflow_name,
        workflow_id=workflow_id,
        input="test",
    )

    await client.get_workflow_result(
        workflow_id=workflow_id,
        run_id=run_id,
    )

    sys.exit(0)


def run_schedule_llm_complete_workflow() -> None:
    asyncio.run(schedule_workflow("LlmCompleteWorkflow"))


if __name__ == "__main__":
    run_schedule_llm_complete_workflow()
