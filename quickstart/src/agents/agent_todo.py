from datetime import timedelta
from typing import List
from pydantic import BaseModel
from restack_ai.agent import agent, import_functions, log
from src.workflows.todo_execute import TodoExecute, TodoExecuteParams


with import_functions():
    from openai import pydantic_function_tool
    from src.functions.llm_chat import llm_chat, LlmChatInput, Message
    from src.functions.todo_create import todo_create, TodoCreateParams

class MessageEvent(BaseModel):
    content: str

class EndEvent(BaseModel):
    end: bool

@agent.defn()
class AgentTodo:
    def __init__(self) -> None:
        self.end = False
        self.messages = []

    @agent.event
    async def message(self, message: MessageEvent) -> List[Message]:
        log.info(f"Received message: {message.content}")

        self.messages.append(Message(role="system", content="You are an AI assistant that creates and execute todos. Eveything the user asks needs to be a todo, that needs to be created and then executed if the user wants to."))

        tools = [pydantic_function_tool(
            model=TodoCreateParams,
            name=todo_create.__name__,
            description="Create a new todo"
        ), pydantic_function_tool(
            model=TodoExecuteParams,
            name=TodoExecute.__name__,
            description="Execute a todo, needs to be created first and need confirmation from user before executing."
        )]

        self.messages.append(Message(role="user", content=message.content or ""))
        completion = await agent.step(llm_chat, LlmChatInput(messages=self.messages, tools=tools), start_to_close_timeout=timedelta(seconds=120))

        log.info(f"completion: {completion}")

        tool_calls = completion.choices[0].message.tool_calls
        self.messages.append(Message(role="assistant", content=completion.choices[0].message.content or "", tool_calls=tool_calls))

        log.info(f"tool_calls: {tool_calls}")

        if tool_calls:
            for tool_call in tool_calls:
                log.info(f"tool_call: {tool_call}")

                name = tool_call.function.name


                match name:
                    case todo_create.__name__:
                        args = TodoCreateParams.model_validate_json(tool_call.function.arguments)

                        # log.info(f"calling {name} with args: {args}")

                        result = await agent.step(todo_create, input=args)
                        self.messages.append(Message(role="tool", tool_call_id=tool_call.id, content=str(result)))

                        completion_with_tool_call = await agent.step(llm_chat, LlmChatInput(messages=self.messages, tools=tools), start_to_close_timeout=timedelta(seconds=120))
                        self.messages.append(Message(role="assistant", content=completion_with_tool_call.choices[0].message.content or ""))
                    case TodoExecute.__name__:
                        args = TodoExecuteParams.model_validate_json(tool_call.function.arguments)

                        # log.info(f"calling {name} with args: {args}")

                        result = await agent.child_execute(TodoExecute, workflow_id=tool_call.id, input=args)
                        self.messages.append(Message(role="tool", tool_call_id=tool_call.id, content=str(result)))

                        completion_with_tool_call = await agent.step(llm_chat, LlmChatInput(messages=self.messages, tools=tools), start_to_close_timeout=timedelta(seconds=120))
                        self.messages.append(Message(role="assistant", content=completion_with_tool_call.choices[0].message.content or ""))

        else:
            self.messages.append(Message(role="assistant", content=completion.choices[0].message.content or ""))

        return self.messages

    @agent.event
    async def end(self, end: EndEvent) -> EndEvent:
        log.info(f"Received end")
        self.end = True
        return {"end": True}

    @agent.run
    async def run(self, input: dict):
        await agent.condition(
            lambda: self.end
        )
        return
