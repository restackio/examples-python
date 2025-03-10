import os
from typing import Literal

from openai import OpenAI
from pydantic import BaseModel, Field
from restack_ai.function import (
    NonRetryableError,
    function,
    stream_to_websocket,
)

from src.client import api_address


class Message(BaseModel):
    role: str
    content: str


class LlmTalkInput(BaseModel):
    messages: list[Message] = Field(default_factory=list)
    context: str | None = None  # Updated context from Slow AI
    mode: Literal["default", "interrupt"]
    stream: bool = True


@function.defn()
async def llm_talk(function_input: LlmTalkInput) -> str:
    """Fast AI generates responses while checking for memory updates."""
    try:
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        common_prompt = (
            "Your are an AI assistant helping developers build with restack: the backend framework for accurate & reliable AI agents."
            "Your interface with users will be voice. Be friendly, helpful and avoid usage of unpronouncable punctuation."
            "Always try to bring back the conversation to restack if the user is talking about something else. "
            "Current context: " + function_input.context
        )

        if function_input.mode == "default":
            system_prompt = (
                common_prompt
                + "If you don't know an answer, **do not make something up**. Instead, be friendly andacknowledge that "
                "you will check for the correct response and let the user know. Keep your answer short in max 20 words"
            )
        else:
            system_prompt = (
                common_prompt
                + "You are providing a short and precise update based on new information. "
                "Do not re-explain everything, just deliver the most important update. Keep your answer short in max 20 words unless the user asks for more information."
            )

        function_input.messages.insert(
            0, Message(role="system", content=system_prompt)
        )

        messages_dicts = [
            msg.model_dump() for msg in function_input.messages
        ]

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages_dicts,
            stream=function_input.stream,
        )

        if function_input.stream:
            return await stream_to_websocket(
                api_address=api_address, data=response
            )
        return response.choices[0].message.content

    except Exception as e:
        raise NonRetryableError(f"llm_talk failed: {e}") from e
