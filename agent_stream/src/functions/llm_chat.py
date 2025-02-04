from restack_ai.function import function, log, stream_to_websocket
from openai import OpenAI
from openai.resources.chat.completions import Stream, ChatCompletionChunk
import os
from pydantic import BaseModel
from typing import Literal, Optional, List
from ..client import api_address

class Message(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str

class LlmChatInput(BaseModel):
    system_content: Optional[str] = None
    model: Optional[str] = None
    messages: Optional[List[Message]] = []

@function.defn()
async def llm_chat(input: LlmChatInput) -> str:
    try:
        client = OpenAI(
            base_url="https://ai.restack.io",
            api_key=os.environ.get("RESTACK_API_KEY")
        )

        if input.system_content:
            input.messages.insert(Message(role="system", content=input.system_content))

        # Convert Message objects to dictionaries
        messages_dicts = [message.model_dump() for message in input.messages]
        # Get the streamed response from OpenAI API
        response: Stream[ChatCompletionChunk] = client.chat.completions.create(
            model=input.model or "restack-c1",
            messages=messages_dicts,
            stream=True,
        )

        # Use Restack API websocket to stream the response
        final_response = await stream_to_websocket("f29d-2a01-5241-ccc-e00-54c9-3c26-c463-b9d8.ngrok-free.app", response)
        return final_response

    except Exception as e:
        log.error("llm_chat function failed", error=str(e))
        raise e