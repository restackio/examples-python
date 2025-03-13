from datetime import timedelta

from pydantic import BaseModel
from restack_ai.agent import (
    NonRetryableError,
    agent,
    import_functions,
    log,
)

from src.workflows.todo_execute import (
    TodoExecute,
    TodoExecuteParams,
)

with import_functions():
    from openai import pydantic_function_tool

    from src.functions.llm_chat import (
        LlmChatInput,
        Message,
        llm_chat,
    )
    from src.functions.todo_create import (
        TodoCreateParams,
        todo_create,
    )


class MessagesEvent(BaseModel):
    messages: list[Message]


class EndEvent(BaseModel):
    end: bool


@agent.defn()
class AgentTodo:
    def __init__(self) -> None:
        self.end = False
        self.messages = [Message(
            role="system",
            content="You are an AI assistant that creates and execute todos. Eveything the user asks needs to be a todo, that needs to be created and then executed if the user wants to.",
        )]


    @agent.event
    async def messages(self, messages_event: MessagesEvent) -> list[Message]:
        try:
            self.messages.extend(messages_event.messages)

            tools = [
                pydantic_function_tool(
                    model=TodoCreateParams,
                    name=todo_create.__name__,
                    description="Create a new todo",
                ),
                pydantic_function_tool(
                    model=TodoExecuteParams,
                    name=TodoExecute.__name__,
                    description="Execute a todo, needs to be created first and need confirmation from user before executing.",
                ),
            ]
            try:
                completion = await agent.step(
                    function=llm_chat,
                    function_input=LlmChatInput(messages=self.messages, tools=tools),
                    start_to_close_timeout=timedelta(seconds=120),
                )
            except Exception as e:
                error_message = f"Error during llm_chat: {e}"
                raise NonRetryableError(error_message) from e
            else:
                log.info(f"completion: {completion}")
                tool_calls = completion.choices[0].message.tool_calls
                self.messages.append(
                    Message(
                        role="assistant",
                        content=completion.choices[0].message.content or "",
                        tool_calls=tool_calls,
                    )
                )

                log.info(f"tool_calls: {tool_calls}")

                if tool_calls:
                    for tool_call in tool_calls:
                        log.info(f"tool_call: {tool_call}")

                        name = tool_call.function.name

                        match name:
                            case todo_create.__name__:
                                args = TodoCreateParams.model_validate_json(
                                    tool_call.function.arguments
                                )

                                try:
                                    result = await agent.step(
                                        function=todo_create,
                                        function_input=args,
                                    )
                                except Exception as e:
                                    error_message = f"Error during todo_create: {e}"
                                    raise NonRetryableError(error_message) from e
                                else:
                                    self.messages.append(
                                        Message(
                                            role="tool",
                                            tool_call_id=tool_call.id,
                                            content=str(result),
                                        )
                                    )
                                    try:
                                        completion_with_tool_call = await agent.step(
                                            function=llm_chat,
                                            function_input=LlmChatInput(
                                                messages=self.messages, tools=tools
                                            ),
                                            start_to_close_timeout=timedelta(seconds=120),
                                        )
                                    except Exception as e:
                                        error_message = f"Error during llm_chat: {e}"
                                        raise NonRetryableError(error_message) from e
                                    else:
                                        self.messages.append(
                                            Message(
                                                role="assistant",
                                                content=completion_with_tool_call.choices[
                                                    0
                                                ].message.content
                                                or "",
                                            )
                                        )
                            case TodoExecute.__name__:
                                args = TodoExecuteParams.model_validate_json(
                                    tool_call.function.arguments
                                )

                                try:
                                    result = await agent.child_execute(
                                        workflow=TodoExecute,
                                        workflow_id=tool_call.id,
                                        workflow_input=args,
                                    )
                                except Exception as e:
                                    error_message = f"Error during TodoExecute: {e}"
                                    raise NonRetryableError(error_message) from e
                                else:
                                    self.messages.append(
                                        Message(
                                            role="tool",
                                            tool_call_id=tool_call.id,
                                            content=str(result),
                                        )
                                    )

                                    try:
                                        completion_with_tool_call = await agent.step(
                                            function=llm_chat,
                                            function_input=LlmChatInput(
                                            messages=self.messages, tools=tools
                                        ),
                                        start_to_close_timeout=timedelta(seconds=120),
                                        )
                                    except Exception as e:
                                        error_message = f"Error during llm_chat: {e}"
                                        raise NonRetryableError(error_message) from e
                                    else:
                                        self.messages.append(
                                            Message(
                                                role="assistant",
                                                content=completion_with_tool_call.choices[
                                                    0
                                                ].message.content
                                                or "",
                                            )
                                        )
                else:
                    self.messages.append(
                        Message(
                            role="assistant",
                            content=completion.choices[0].message.content or "",
                        )
                    )
        except Exception as e:
            log.error(f"Error during message event: {e}")
            raise
        else:
            return self.messages

    @agent.event
    async def end(self) -> EndEvent:
        log.info("Received end")
        self.end = True
        return {"end": True}

    @agent.run
    async def run(self, function_input: dict) -> None:
        log.info("AgentTodo function_input", function_input=function_input)
        await agent.condition(lambda: self.end)
