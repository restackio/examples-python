from datetime import timedelta

from pydantic import BaseModel
from restack_ai.agent import (
    NonRetryableError,
    agent,
    import_functions,
    log,
)

with import_functions():
    from src.functions.context_docs import context_docs
    from src.functions.llm_chat import (
        LlmChatInput,
        Message,
        llm_chat,
    )
    from src.functions.daily_send_data import daily_send_data, DailySendDataInput


class MessagesEvent(BaseModel):
    messages: list[Message]


class EndEvent(BaseModel):
    end: bool

class AgentInput(BaseModel):
    room_url: str

class DailyMessageEvent(BaseModel):
    message: str
    recipient: str | None = None


@agent.defn()
class AgentVideo:
    def __init__(self) -> None:
        self.end = False
        self.messages: list[Message] = []
        self.room_url = ""

    @agent.event
    async def messages(
        self,
        messages_event: MessagesEvent,
    ) -> list[Message]:
        log.info(f"Received message: {messages_event.messages}")
        self.messages.extend(messages_event.messages)

        try:
            assistant_message = await agent.step(
                function=llm_chat,
                function_input=LlmChatInput(
                    messages=self.messages,
                ),
                start_to_close_timeout=timedelta(seconds=120),
            )
        except Exception as e:
            error_message = f"llm_chat function failed: {e}"
            raise NonRetryableError(error_message) from e
        else:
            self.messages.append(
                Message(
                    role="assistant",
                    content=str(assistant_message),
                ),
            )
            return self.messages

    @agent.event
    async def end(self, end: EndEvent) -> EndEvent:
        log.info("Received end")
        self.end = True
        return end

    @agent.event
    async def daily_message(self, daily_message: DailyMessageEvent) -> bool:
        log.info("Received message", daily_message=daily_message)
        await agent.step(
            function=daily_send_data,
            function_input=DailySendDataInput(
                room_url=self.room_url,
                data={"text": daily_message.message, "author": "agent"},
                recipient=daily_message.recipient,
            ),
        )
        return True

    @agent.run
    async def run(self, agent_input: AgentInput) -> None:
        try:
            self.room_url = agent_input.room_url
            docs = await agent.step(function=context_docs)
        except Exception as e:
            error_message = f"context_docs function failed: {e}"
            raise NonRetryableError(error_message) from e
        else:
            system_prompt = f"""
            You are an interactive video assistant, your answers will be used in text to speech so try to keep answers short and concise so that interaction is seamless.
            You can answer questions about the following documentation:
            {docs}
            """
            self.messages.append(
                Message(role="system", content=system_prompt),
            )

            await agent.condition(lambda: self.end)
