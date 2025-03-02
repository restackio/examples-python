from datetime import timedelta

from pydantic import BaseModel, Field
from restack_ai.agent import agent, import_functions, log

with import_functions():
    from src.functions.livekit_dispatch import LivekitDispatchInput, livekit_dispatch
    from src.functions.llm_chat import LlmChatInput, Message, llm_chat


class MessagesEvent(BaseModel):
    messages: list[Message]


class EndEvent(BaseModel):
    end: bool


class AgentVoiceInput(BaseModel):
    room_id: str | None = Field(default="room-1")

@agent.defn()
class AgentVoice:
    def __init__(self) -> None:
        self.end = False
        self.messages: list[Message] = []

    @agent.event
    async def messages(self, messages_event: MessagesEvent) -> list[Message]:
        log.info(f"Received message: {messages_event.messages}")
        self.messages.extend(messages_event.messages)

        assistant_message = await agent.step(
            function=llm_chat,
            function_input=LlmChatInput(messages=self.messages),
            start_to_close_timeout=timedelta(minutes=2),
        )
        self.messages.append(Message(role="assistant", content=str(assistant_message)))
        return self.messages

    @agent.event
    async def end(self, end: EndEvent) -> EndEvent:
        log.info("Received end")
        self.end = True
        return end

    @agent.run
    async def run(self, agent_input: AgentVoiceInput) -> None:
        log.info("Run", agent_input=agent_input)
        room_id = agent_input.room_id

        await agent.step(
            function=livekit_dispatch,
            function_input=LivekitDispatchInput(room_id=room_id),
        )
        await agent.condition(lambda: self.end)
