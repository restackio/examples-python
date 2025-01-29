import asyncio
from restack_ai import Restack
async def main(workflow_id:str,run_id:str):

    client = Restack()

    await client.send_workflow_event(
        workflow_id=workflow_id,
        run_id=run_id,
        event_name="message",
        event_input={"content": "Tell me another joke"}
    )

    await client.send_workflow_event(
        workflow_id=workflow_id,
        run_id=run_id,
        event_name="end",
    )

    exit(0)

def run_event_workflow():
    asyncio.run(main(workflow_id="your-workflow-id", run_id="your-run-id"))

if __name__ == "__main__":
    run_event_workflow()