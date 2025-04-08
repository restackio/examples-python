from datetime import timedelta
from typing import Literal

from pydantic import BaseModel
from restack_ai.agent import (
    NonRetryableError,
    RetryPolicy,
    agent,
    import_functions,
    log,
    uuid,
)

from src.workflows.logic import LogicWorkflow, LogicWorkflowInput

with import_functions():
    from src.functions.context_docs import context_docs
    from src.functions.daily_send_data import (
        DailySendDataInput,
        daily_send_data,
    )
    from src.functions.llm_chat import (
        LlmChatInput,
        Message,
        llm_chat,
    )
    from src.functions.llm_talk import LlmTalkInput, llm_talk


class MessagesEvent(BaseModel):
    messages: list[Message]


class EndEvent(BaseModel):
    end: bool


class AgentInput(BaseModel):
    room_url: str
    model: Literal["restack", "gpt-4o-mini", "gpt-4o", "openpipe:twenty-lions-fall"] = "restack"
    interactive_prompt: str | None = None
    reasoning_prompt: str | None = None


class ContextEvent(BaseModel):
    context: str


class DailyMessageEvent(BaseModel):
    message: str
    recipient: str | None = None


@agent.defn()
class AgentVideo:
    def __init__(self) -> None:
        self.end = False
        self.messages: list[Message] = []
        self.room_url = ""
        self.model: Literal[
            "restack", "gpt-4o-mini", "gpt-4o", "openpipe:twenty-lions-fall", "ft:gpt-4o-mini-2024-07-18:restack::BJymdMm8"
        ] = "restack"
        self.interactive_prompt = ""
        self.reasoning_prompt = ""
        self.context = ""

    @agent.event
    async def messages(
        self,
        messages_event: MessagesEvent,
    ) -> list[Message]:
        log.info(f"Received message: {messages_event.messages}")
        self.messages.extend(messages_event.messages)
        try:
            await agent.child_start(
                workflow=LogicWorkflow,
                workflow_id=f"{uuid()}-logic",
                workflow_input=LogicWorkflowInput(
                    messages=self.messages,
                    room_url=self.room_url,
                    context=str(self.context),
                    interactive_prompt=self.interactive_prompt,
                    reasoning_prompt=self.reasoning_prompt,
                    model=self.model,
                ),
            )

            assistant_message = await agent.step(
                function=llm_talk,
                function_input=LlmTalkInput(
                    messages=self.messages[-3:],
                    context=str(self.context),
                    mode="default",
                    model=self.model,
                    interactive_prompt=self.interactive_prompt,
                ),
                start_to_close_timeout=timedelta(seconds=3),
                retry_policy=RetryPolicy(
                    initial_interval=timedelta(seconds=1),
                    maximum_attempts=1,
                    maximum_interval=timedelta(seconds=5),
                ),
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
    async def context(self, context: ContextEvent) -> str:
        log.info("Received context")
        self.context = context.context
        return self.context

    @agent.event
    async def daily_message(
        self, daily_message: DailyMessageEvent
    ) -> bool:
        log.info("Received message", daily_message=daily_message)
        await agent.step(
            function=daily_send_data,
            function_input=DailySendDataInput(
                room_url=self.room_url,
                data={
                    "text": daily_message.message,
                    "author": "agent",
                },
                recipient=daily_message.recipient,
            ),
        )
        return True

    @agent.run
    async def run(self, agent_input: AgentInput) -> None:
        try:
            self.room_url = agent_input.room_url
            self.model = agent_input.model
            self.interactive_prompt = (
                agent_input.interactive_prompt
            )
            self.reasoning_prompt = agent_input.reasoning_prompt
            docs = await agent.step(function=context_docs)
        except Exception as e:
            error_message = f"context_docs function failed: {e}"
            raise NonRetryableError(error_message) from e
        else:
            system_prompt = f"""
            You are an AI assistant for Restack. You can answer questions about the following documentation:
            {docs}
            {self.interactive_prompt}
            """
            self.messages.append(
                Message(role="system", content=system_prompt),
            )

            await agent.condition(lambda: self.end)
