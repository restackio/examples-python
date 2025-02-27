from datetime import timedelta

from pydantic import BaseModel, Field
from restack_ai.agent import agent, agent_info, import_functions, log

with import_functions():
    from src.functions.livekit_call import LivekitCallInput, livekit_call
    from src.functions.livekit_dispatch import LivekitDispatchInput, livekit_dispatch
    from src.functions.livekit_outbound_trunk import livekit_outbound_trunk
    from src.functions.livekit_room import livekit_room
    from src.functions.llm_chat import LlmChatInput, Message, llm_chat


class MessagesEvent(BaseModel):
    messages: list[Message]


class EndEvent(BaseModel):
    end: bool


class AgentStreamInput(BaseModel):
    room_id: str | None = Field(default="room-1")


@agent.defn()
class AgentStream:
    def __init__(self) -> None:
        self.end = False
        self.messages: list[Message] = []
        self.room_id = ""
        self.prospect_phone_number = "+491704675288"

    @agent.event
    async def messages(self, messages_event: MessagesEvent) -> list[Message]:
        log.info(f"Received message: {messages_event.messages}")
        self.messages.extend(messages_event.messages)

        assistant_message = await agent.step(
            function=llm_chat,
            function_input=LlmChatInput(messages=self.messages),
            start_to_close_timeout=timedelta(seconds=120),
        )
        self.messages.append(Message(role="assistant", content=str(assistant_message)))
        return self.messages

    @agent.event
    async def call(self, call_input: dict) -> None:
        log.info("Call", call_input=call_input)
        phone_number = self.prospect_phone_number
        agent_name = agent_info().workflow_type
        agent_id = agent_info().workflow_id
        run_id = agent_info().run_id
        sip_trunk_id = await agent.step(function=livekit_outbound_trunk)
        return await agent.step(
            function=livekit_call,
            function_input=LivekitCallInput(
                sip_trunk_id=sip_trunk_id,
                phone_number=phone_number,
                room_id=self.room_id,
                agent_name=agent_name,
                agent_id=agent_id,
                run_id=run_id,
            ),
        )

    @agent.run
    async def run(self, agent_input: AgentStreamInput) -> None:
        log.info("Run", agent_input=agent_input)
        self.room_id = agent_input.room_id

        if not self.room_id:
            room = await agent.step(function=livekit_room)
            self.room_id = room.name

        await agent.step(
            function=livekit_dispatch,
            function_input=LivekitDispatchInput(room_id=self.room_id),
        )
        await agent.condition(lambda: self.end)


    @agent.event
    async def end(self, end: EndEvent) -> EndEvent:
        log.info("Received end")
        self.end = True
        return end