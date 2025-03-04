from datetime import timedelta

from pydantic import BaseModel
from restack_ai.agent import agent, import_functions, log, AgentError

with import_functions():
    from src.functions.llm_chat import LlmChatInput, Message, llm_chat


class MessagesEvent(BaseModel):
    messages: list[Message]


class EndEvent(BaseModel):
    end: bool


@agent.defn()
class AgentChat:
    def __init__(self) -> None:
        self.end = False
        self.messages = []

    @agent.event
    async def messages(self, messages_event: MessagesEvent) -> list[Message]:
        try:
            log.info(f"Received messages: {messages_event.messages}")
            self.messages.extend(messages_event.messages)
            
            log.info(f"Calling llm_chat with messages: {self.messages}")
            assistant_message = await agent.step(
                function=llm_chat,
                function_input=LlmChatInput(messages=self.messages),
                start_to_close_timeout=timedelta(seconds=120),
            )
          
            self.messages.append(assistant_message)
            return self.messages
        except Exception as e:
                log.error(f"Error in messages: {e}")
                raise AgentError(f"Error in messages: {e}")

    @agent.event
    async def end(self, end: EndEvent) -> EndEvent:
        log.info("Received end")
        self.end = True
        return end

    @agent.run
    async def run(self, function_input: dict) -> None:
        log.info("AgentChat function_input", function_input=function_input)
        await agent.condition(lambda: self.end)
