from dataclasses import dataclass
from datetime import timedelta
from typing import List
from pydantic import BaseModel
from restack_ai.agent import agent, import_functions, log, agent_info

with import_functions():
    from src.functions.llm_chat import llm_chat, LlmChatInput, Message
    from src.functions.livekit_dispatch import livekit_dispatch, LivekitDispatchInput
    from src.functions.livekit_token import livekit_token, LivekitTokenInput, LivekitTokenOutput
    from src.functions.livekit_call import livekit_call, LivekitCallInput
    from src.functions.livekit_room import livekit_room
    from src.functions.livekit_outbound_trunk import livekit_outbound_trunk
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
        self.room_id = ""
        self.prospect_phone_number = "+491704675288"

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

    @agent.event
    async def join(self, join_input: dict) -> LivekitTokenOutput:
        agent_name = agent_info().workflow_type
        agent_id = agent_info().workflow_id
        run_id = agent_info().run_id
        livekit_response =await agent.step(livekit_token, LivekitTokenInput(agent_name=agent_name, agent_id=agent_id, run_id=run_id))
        return livekit_response
    
    @agent.event
    async def call(self, call_input: dict) -> None:
        phone_number = self.prospect_phone_number
        agent_name = agent_info().workflow_type
        agent_id = agent_info().workflow_id
        run_id = agent_info().run_id
        sip_trunk_id = await agent.step(livekit_outbound_trunk)
        livekit_response = await agent.step(livekit_call, LivekitCallInput(sip_trunk_id=sip_trunk_id,phone_number=phone_number,room_id=self.room_id,agent_name=agent_name, agent_id=agent_id, run_id=run_id))
        return livekit_response
    
    @agent.run
    async def run(self, agent_input:AgentStreamInput):
        
        self.room_id = agent_input.room_id

        if not self.room_id:
            room = await agent.step(livekit_room)
            self.room_id = room.name
        
        await agent.step(livekit_dispatch, LivekitDispatchInput(room_id=self.room_id))
        await agent.condition(lambda: self.end)
        return


