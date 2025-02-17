import asyncio
import sys
import time

from restack_ai import Restack


async def main() -> None:
    client = Restack()

    agent_id = f"{int(time.time() * 1000)}-AgentChat"
    await client.schedule_agent(agent_name="AgentChat", agent_id=agent_id)

    sys.exit(0)


def run_schedule_agent() -> None:
    asyncio.run(main())


if __name__ == "__main__":
    run_schedule_agent()
