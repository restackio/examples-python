import asyncio
import sys

from restack_ai import Restack


async def main(agent_id: str, run_id: str) -> None:
    client = Restack()

    await client.send_agent_event(
        agent_id=agent_id,
        run_id=run_id,
        event_name="message",
        event_input={"content": "Tell me another joke"},
    )

    await client.send_agent_event(
        agent_id=agent_id,
        run_id=run_id,
        event_name="end",
    )

    sys.exit(0)


def run_event_agent() -> None:
    asyncio.run(
        main(
            agent_id="1739788461173-AgentChat",
            run_id="c3937cc9-8d88-4e37-85e1-59e78cf1bf60",
        )
    )


if __name__ == "__main__":
    run_event_agent()
