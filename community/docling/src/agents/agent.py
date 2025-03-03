from pydantic import BaseModel
from restack_ai.agent import (
    agent,
    log,
)

class EndEvent(BaseModel):
    end: bool

class AgentInput(BaseModel):
    test_input: str | None = None

@agent.defn()
class Agent:
    def __init__(self) -> None:
        self.end = False

    @agent.event
    async def end(self, end: EndEvent) -> EndEvent:
        log.info("Received end")
        self.end = True
        return end

    @agent.run
    async def run(self, agent_input: AgentInput):
        log.info("Received agent input", agent_input=agent_input)
        await agent.condition(lambda: self.end)