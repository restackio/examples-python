from datetime import timedelta

from pydantic import BaseModel
from restack_ai.agent import (
    NonRetryableError,
    agent,
    import_functions,
    log,
)

with import_functions():
    from src.functions.llm_chat import (
        LlmChatInput,
        Message,
        llm_chat,
    )
    from src.functions.lookup_sales import lookup_sales


class MessagesEvent(BaseModel):
    messages: list[Message]


class EndEvent(BaseModel):
    end: bool


@agent.defn()
class AgentRag:
    def __init__(self) -> None:
        self.end = False
        self.messages = []

    @agent.event
    async def messages(self, messages_event: MessagesEvent) -> list[Message]:
        log.info(f"Received messages: {messages_event.messages}")
        self.messages.extend(messages_event.messages)
        try:
            sales_info = await agent.step(
                function=lookup_sales, start_to_close_timeout=timedelta(seconds=120)
            )
        except Exception as e:
            error_message = f"Error during lookup_sales: {e}"
            raise NonRetryableError(error_message) from e
        else:
            system_content = f"You are a helpful assistant that can help with sales data. Here is the sales information: {sales_info}"

            try:
                completion = await agent.step(
                    function=llm_chat,
                    function_input=LlmChatInput(
                        messages=self.messages, system_content=system_content
                    ),
                    start_to_close_timeout=timedelta(seconds=120),
                )
            except Exception as e:
                error_message = f"Error during llm_chat: {e}"
                raise NonRetryableError(error_message) from e
            else:
                log.info(f"completion: {completion}")
                self.messages.append(
                    Message(
                        role="assistant", content=completion.choices[0].message.content or ""
                    )
                )

                return self.messages

    @agent.event
    async def end(self) -> EndEvent:
        log.info("Received end")
        self.end = True
        return {"end": True}

    @agent.run
    async def run(self, function_input: dict) -> None:
        log.info("AgentRag function_input", function_input=function_input)
        await agent.condition(lambda: self.end)
