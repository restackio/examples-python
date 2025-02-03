import asyncio
import time
from restack_ai import Restack
from agent_chat.src.agents.agent import AgentChatInput
async def main():

    client = Restack()

    workflow_id = f"{int(time.time() * 1000)}-AgentChat"
    run_id = await client.schedule_agent(
        agent_name="AgentChat",
        agent_id=workflow_id,
        input=AgentChatInput(message="Tell me a joke")
    ) 

    await client.get_agent_result(
        agent_id=workflow_id,
        run_id=run_id
    )

    exit(0)

def run_schedule_agent():
    asyncio.run(main())

if __name__ == "__main__":
    run_schedule_agent()