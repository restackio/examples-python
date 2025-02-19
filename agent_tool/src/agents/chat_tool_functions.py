from datetime import timedelta

from pydantic import BaseModel
from restack_ai.agent import agent, import_functions, log

with import_functions():
    from openai import pydantic_function_tool

    from src.functions.llm_chat import LlmChatInput, Message, llm_chat
    from src.functions.lookup_sales import LookupSalesInput, lookup_sales


class MessageEvent(BaseModel):
    content: str


class EndEvent(BaseModel):
    end: bool


@agent.defn()
class AgentChatToolFunctions:
    def __init__(self) -> None:
        self.end = False
        self.messages = []

    @agent.event
    async def message(self, message: MessageEvent) -> list[Message]:
        log.info(f"Received message: {message.content}")

        tools = [
            pydantic_function_tool(
                model=LookupSalesInput,
                name=lookup_sales.__name__,
                description="Lookup sales for a given category",
            ),
        ]

        system_content = "You are a helpful assistant that can help with sales data."

        self.messages.append(Message(role="user", content=message.content or ""))
        completion = await agent.step(
            function=llm_chat,
            function_input=LlmChatInput(
                messages=self.messages, tools=tools, system_content=system_content
            ),
            start_to_close_timeout=timedelta(seconds=120),
        )

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
                    case lookup_sales.__name__:
                        args = LookupSalesInput.model_validate_json(
                            tool_call.function.arguments
                        )

                        log.info(f"calling {name} with args: {args}")

                        result = await agent.step(
                            function=lookup_sales,
                            function_input=LookupSalesInput(category=args.category),
                            start_to_close_timeout=timedelta(seconds=120),
                        )
                        self.messages.append(
                            Message(
                                role="tool",
                                tool_call_id=tool_call.id,
                                content=str(result),
                            )
                        )

                        completion_with_tool_call = await agent.step(
                            function=llm_chat,
                            function_input=LlmChatInput(
                                messages=self.messages, system_content=system_content
                            ),
                            start_to_close_timeout=timedelta(seconds=120),
                        )
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
            pass

        return self.messages

    @agent.event
    async def end(self) -> EndEvent:
        log.info("Received end")
        self.end = True
        return {"end": True}

    @agent.run
    async def run(self, function_input: dict) -> None:
        await agent.condition(lambda: self.end)
