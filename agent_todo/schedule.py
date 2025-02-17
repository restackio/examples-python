import asyncio
import sys
import time

from restack_ai import Restack
from src.agents.agent_todo import AgentTodo


async def main() -> None:
    client = Restack()

    agent_id = f"{int(time.time() * 1000)}-{AgentTodo.__name__}"
    run_id = await client.schedule_agent(
        agent_name=AgentTodo.__name__,
        agent_id=agent_id,
        input=AgentTodo(),
    )

    await client.get_agent_result(agent_id=agent_id, run_id=run_id)

    sys.exit(0)


def run_schedule() -> None:
    asyncio.run(main())


if __name__ == "__main__":
    run_schedule()
