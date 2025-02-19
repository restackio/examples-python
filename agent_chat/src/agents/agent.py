from datetime import timedelta

from pydantic import BaseModel
from restack_ai.agent import agent, import_functions, log

with import_functions():
    from src.functions.llm_chat import LlmChatInput, Message, llm_chat


class MessageEvent(BaseModel):
    content: str


class EndEvent(BaseModel):
    end: bool


@agent.defn()
class AgentChat:
    def __init__(self) -> None:
        self.end = False
        self.messages = []

    @agent.event
    async def message(self, message: MessageEvent) -> list[Message]:
        log.info(f"Received message: {message.content}")
        self.messages.append({"role": "user", "content": message.content})
        assistant_message_raw = await agent.step(
            function=llm_chat,
            function_input=LlmChatInput(messages=self.messages),
            start_to_close_timeout=timedelta(seconds=120),
        )
        assistant_message = {
            "role": assistant_message_raw.choices[0].message.role,
            "content": assistant_message_raw.choices[0].message.content,
        }
        self.messages.append(assistant_message)
        return self.messages

    @agent.event
    async def end(self, end: EndEvent) -> EndEvent:
        log.info("Received end")
        self.end = True
        return end

    @agent.run
    async def run(self, function_input: dict) -> None:
        await agent.condition(lambda: self.end)
