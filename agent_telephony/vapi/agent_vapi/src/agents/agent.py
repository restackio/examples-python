from datetime import timedelta

from pydantic import BaseModel
from restack_ai.agent import NonRetryableError, agent, import_functions, log

with import_functions():
    from src.functions.llm_chat import LlmChatInput, Message, llm_chat
    from src.functions.vapi_call import VapiCallInput, vapi_call


class MessagesEvent(BaseModel):
    messages: list[Message]


class EndEvent(BaseModel):
    end: bool


class CallInput(BaseModel):
    assistant_id: str
    phone_number: str


@agent.defn()
class AgentVapi:
    def __init__(self) -> None:
        self.end = False
        self.messages: list[Message] = []

    @agent.event
    async def messages(self, messages_event: MessagesEvent) -> list[Message]:
        log.info(f"Received message: {messages_event.messages}")
        self.messages.extend(messages_event.messages)

        try:
            assistant_message = await agent.step(
                function=llm_chat,
                function_input=LlmChatInput(messages=self.messages),
                start_to_close_timeout=timedelta(seconds=120),
            )
        except Exception as e:
            error_message = f"llm_chat function failed: {e}"
            raise NonRetryableError(error_message) from e
        else:
            self.messages.append(
                Message(role="assistant", content=str(assistant_message))
            )
            return self.messages

    @agent.event
    async def call(self, call_input: CallInput) -> None:
        log.info("Call", call_input=call_input)
        assistant_id = call_input.assistant_id
        phone_number = call_input.phone_number

        try:
            result = agent.step(
                function=vapi_call,
                function_input=VapiCallInput(
                    assistant_id=assistant_id,
                    phone_number=phone_number,
                ),
            )
        except Exception as e:
            error_message = f"vapi_call function failed: {e}"
            raise NonRetryableError(error_message) from e
        else:
            return result

    @agent.event
    async def end(self, end: EndEvent) -> EndEvent:
        log.info("Received end")
        self.end = True
        return end

    @agent.run
    async def run(self) -> None:
        await agent.condition(lambda: self.end)
