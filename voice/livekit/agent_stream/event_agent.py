import asyncio
import sys

from restack_ai import Restack


async def main(agent_id: str, run_id: str) -> None:
    client = Restack()

    await client.send_agent_event(
        agent_id=agent_id,
        run_id=run_id,
        event_name="messages",
        event_input={"messages": [{"role": "user", "content": "Tell me another joke"}]},
    )

    await client.send_agent_event(
        agent_id=agent_id,
        run_id=run_id,
        event_name="end",
    )

    sys.exit(0)


def run_event_workflow() -> None:
    asyncio.run(main(agent_id="your-agent-id", run_id="your-run-id"))


if __name__ == "__main__":
    run_event_workflow()
