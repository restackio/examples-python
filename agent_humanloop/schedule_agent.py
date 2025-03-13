import asyncio
import time

from restack_ai import Restack


async def main():

    client = Restack()

    agent_id = f"{int(time.time() * 1000)}-AgentHumanLoop"
    runId = await client.schedule_agent(
        agent_name="AgentHumanLoop",
        agent_id=agent_id
    )

    await client.send_agent_event(
        event_name="event_feedback",
        event_input={
            "feedback": "This is a human feedback"
        },
        agent_id=agent_id,
        run_id=runId,
    )

    end = await client.send_agent_event(
        event_name="event_end",
        event_input={
            "end": True
        },
        agent_id=agent_id,
        run_id=runId,
    )

    exit(0)

def run_schedule_workflow():
    asyncio.run(main())

if __name__ == "__main__":
    run_schedule_workflow()
