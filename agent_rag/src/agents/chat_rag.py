from datetime import timedelta
from typing import List
from pydantic import BaseModel
from restack_ai.agent import agent, import_functions, log


with import_functions():
    from src.functions.llm_chat import llm_chat, LlmChatInput, Message
    from src.functions.lookup_sales import lookupSales


class MessageEvent(BaseModel):
    content: str


class EndEvent(BaseModel):
    end: bool


@agent.defn()
class AgentRag:
    def __init__(self) -> None:
        self.end = False
        self.messages = []

    @agent.event
    async def message(self, message: MessageEvent) -> List[Message]:
        log.info(f"Received message: {message.content}")

        sales_info = await agent.step(
            lookupSales, start_to_close_timeout=timedelta(seconds=120)
        )

        system_content = f"You are a helpful assistant that can help with sales data. Here is the sales information: {sales_info}"

        self.messages.append(Message(role="user", content=message.content or ""))

        completion = await agent.step(
            llm_chat,
            LlmChatInput(messages=self.messages, system_content=system_content),
            start_to_close_timeout=timedelta(seconds=120),
        )

        log.info(f"completion: {completion}")

        self.messages.append(
            Message(
                role="assistant", content=completion.choices[0].message.content or ""
            )
        )

        return self.messages

    @agent.event
    async def end(self, end: EndEvent) -> EndEvent:
        log.info("Received end")
        self.end = True
        return {"end": True}

    @agent.run
    async def run(self, input: dict):
        await agent.condition(lambda: self.end)
        return
