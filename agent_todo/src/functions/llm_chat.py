from restack_ai.function import function, log, FunctionFailure
from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion
from openai.types.chat.chat_completion_message_tool_call import (
    ChatCompletionMessageToolCall,
)
from openai.types.chat.chat_completion_tool_param import ChatCompletionToolParam
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Literal, Optional, List

load_dotenv()


class Message(BaseModel):
    role: Literal["system", "user", "assistant", "tool"]
    content: str
    tool_call_id: Optional[str] = None
    tool_calls: Optional[List[ChatCompletionMessageToolCall]] = None


class LlmChatInput(BaseModel):
    system_content: Optional[str] = None
    model: Optional[str] = None
    messages: Optional[List[Message]] = None
    tools: Optional[List[ChatCompletionToolParam]] = None


@function.defn()
async def llm_chat(input: LlmChatInput) -> ChatCompletion:
    try:
        log.info("llm_chat function started", input=input)

        if (os.environ.get("RESTACK_API_KEY") is None):
            raise FunctionFailure("RESTACK_API_KEY is not set", non_retryable=True)

        client = OpenAI(
            base_url="https://ai.restack.io", api_key=os.environ.get("RESTACK_API_KEY")
        )

        log.info("pydantic_function_tool", tools=input.tools)

        if input.system_content:
            input.messages.append(
                Message(role="system", content=input.system_content or "")
            )

        response = client.chat.completions.create(
            model=input.model or "gpt-4o-mini",
            messages=input.messages,
            tools=input.tools,
        )
        return response
    except Exception as e:
        log.error("llm_chat function failed", error=e)
        raise e
