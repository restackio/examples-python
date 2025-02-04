from datetime import timedelta
from typing import List
from pydantic import BaseModel
from restack_ai.agent import agent, import_functions, log

with import_functions():
    from src.functions.llm_chat import llm_chat, LlmChatInput, Message

class MessageEvent(BaseModel):
    content: str

class EndEvent(BaseModel):
    end: bool

@agent.defn()
class AgentStream:
    def __init__(self) -> None:
        self.end = False
        self.messages = []
    @agent.event
    async def message(self, message: MessageEvent) -> List[Message]:
        log.info(f"Received message: {message.content}")
        self.messages.append(Message(role="user", content=message.content))
        assistant_message = await agent.step(llm_chat, LlmChatInput(messages=self.messages), start_to_close_timeout=timedelta(seconds=120))
        self.messages.append(Message(role="assistant", content=str(assistant_message)))
        return self.messages
    @agent.event
    async def end(self, end: EndEvent) -> EndEvent:
        log.info(f"Received end")
        self.end = True
        return end
    @agent.run
    async def run(self, input: dict):
        await agent.condition(
            lambda: self.end
        )
        return


