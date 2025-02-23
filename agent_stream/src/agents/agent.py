from dataclasses import dataclass
from datetime import timedelta
from typing import List
from pydantic import BaseModel
from restack_ai.agent import agent, import_functions, log

with import_functions():
    from src.functions.llm_chat import llm_chat, LlmChatInput, Message
class MessagesEvent(BaseModel):
    messages: List[Message]

class EndEvent(BaseModel):
    end: bool

@dataclass
class AgentStreamInput:
    room_id: str | None = None

@agent.defn()
class AgentStream:
    def __init__(self) -> None:
        self.end = False
        self.messages: List[Message] = []

    @agent.event
    async def messages(self, messages_event: MessagesEvent) -> List[Message]:
        log.info(f"Received message: {messages_event.messages}")
        self.messages.extend(messages_event.messages)
        
        assistant_message = await agent.step(
            llm_chat,
            LlmChatInput(messages=self.messages),
            start_to_close_timeout=timedelta(seconds=120)
        )
        self.messages.append(Message(role="assistant", content=str(assistant_message)))
        return self.messages

    @agent.event
    async def end(self, end: EndEvent) -> EndEvent:
        log.info("Received end")
        self.end = True
        return end
    
    @agent.run
    async def run(self, agent_input:AgentStreamInput):
        return

