from datetime import timedelta
from typing import List
from pydantic import BaseModel
from restack_ai.workflow import workflow, import_functions, log

with import_functions():
    from src.functions.llm_chat import llm_chat, LlmChatInput, Message

class MessageEvent(BaseModel):
    content: str

class EndEvent(BaseModel):
    end: bool

@workflow.defn()
class AgentChat:
    def __init__(self) -> None:
        self.end = False
        self.messages = []
    @workflow.event
    async def message(self, message: MessageEvent) -> List[Message]:
        log.info(f"Received message: {message.content}")
        self.messages.append({"role": "user", "content": message.content})
        assistant_message = await workflow.step(llm_chat, LlmChatInput(messages=self.messages), start_to_close_timeout=timedelta(seconds=120))
        self.messages.append(assistant_message)
        return self.messages
    @workflow.event
    async def end(self, end: EndEvent) -> EndEvent:
        log.info(f"Received end")
        self.end = True
        return end
    @workflow.run
    async def run(self, input: dict):
        await workflow.condition(
            lambda: self.end
        )
        return


