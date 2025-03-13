import os
from typing import Literal

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion
from openai.types.chat.chat_completion_message_tool_call import (
    ChatCompletionMessageToolCall,
)
from openai.types.chat.chat_completion_tool_param import (
    ChatCompletionToolParam,
)
from pydantic import BaseModel
from restack_ai.function import NonRetryableError, function, log

load_dotenv()


class Message(BaseModel):
    role: Literal["system", "user", "assistant", "tool"]
    content: str
    tool_call_id: str | None = None
    tool_calls: list[ChatCompletionMessageToolCall] | None = None


class LlmChatInput(BaseModel):
    system_content: str | None = None
    model: str | None = None
    messages: list[Message] | None = None
    tools: list[ChatCompletionToolParam] | None = None


def raise_exception(message: str) -> None:
    log.error(message)
    raise NonRetryableError(message)


@function.defn()
async def llm_chat(function_input: LlmChatInput) -> ChatCompletion:
    try:
        log.info("llm_chat function started", function_input=function_input)

        if os.environ.get("RESTACK_API_KEY") is None:
            raise_exception("RESTACK_API_KEY is not set")

        client = OpenAI(
            base_url="https://ai.restack.io", api_key=os.environ.get("RESTACK_API_KEY")
        )

        log.info("pydantic_function_tool", tools=function_input.tools)

        if function_input.system_content:
            function_input.messages.append(
                Message(role="system", content=function_input.system_content or "")
            )

        result = client.chat.completions.create(
            model=function_input.model or "gpt-4o-mini",
            messages=function_input.messages,
            tools=function_input.tools,
        )

        log.info("llm_chat function completed", result=result)

        return result.model_dump()
    except Exception as e:
        error_message = f"LLM chat failed: {e}"
        raise NonRetryableError(error_message) from e
