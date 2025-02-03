import asyncio
from restack_ai import Restack
async def main(agent_id:str,run_id:str):

    client = Restack()

    await client.send_agent_event(
        agent_id=agent_id,
        run_id=run_id,
        event_name="message",
        event_input={"content": "Tell me another joke"}
    )

    await client.send_agent_event(
        agent_id=agent_id,
        run_id=run_id,
        event_name="end",
    )

    exit(0)

def run_event_agent():
    asyncio.run(main(agent_id="your-agent-id", run_id="your-run-id"))

if __name__ == "__main__":
    run_event_agent()