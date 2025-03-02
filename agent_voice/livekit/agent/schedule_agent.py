import asyncio
import sys
import time

from restack_ai import Restack
from src.agents.agent import AgentVoice


async def main(room_id: str) -> None:
    client = Restack()

    agent_id = f"{int(time.time() * 1000)}-{AgentVoice.__name__}"
    run_id = await client.schedule_agent(
        agent_name=AgentVoice.__name__,
        agent_id=agent_id,
        agent_input={"room_id": room_id},
    )

    await client.get_agent_result(agent_id=agent_id, run_id=run_id)

    sys.exit(0)


def run_schedule_agent() -> None:
    asyncio.run(main(room_id="room-id"))


if __name__ == "__main__":
    run_schedule_agent()
