import os
from typing import TYPE_CHECKING, Literal

from openai import OpenAI
from pydantic import BaseModel, Field
from restack_ai.function import function, log, stream_to_websocket

from src.client import api_address

if TYPE_CHECKING:
    from openai.resources.chat.completions import ChatCompletionChunk, Stream


class Message(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str


class LlmChatInput(BaseModel):
    system_content: str | None = None
    model: str | None = None
    messages: list[Message] = Field(default_factory=list)
    stream: bool = True


@function.defn()
async def llm_chat(function_input: LlmChatInput) -> str:
    try:
        client = OpenAI(
            base_url="https://ai.restack.io", api_key=os.environ.get("RESTACK_API_KEY")
        )

        if function_input.system_content:
            # Insert the system message at the beginning
            function_input.messages.insert(
                0, Message(role="system", content=function_input.system_content)
            )

        # Convert Message objects to dictionaries
        messages_dicts = [message.model_dump() for message in function_input.messages]
        # Get the streamed response from OpenAI API
        response: Stream[ChatCompletionChunk] = client.chat.completions.create(
            model=function_input.model or "gpt-4o-mini",
            messages=messages_dicts,
            stream=True,
        )

        # Use Restack API websocket to stream the response
        return await stream_to_websocket(api_address=api_address, data=response)

    except Exception as e:
        log.error("llm_chat function failed", error=str(e))
        raise
