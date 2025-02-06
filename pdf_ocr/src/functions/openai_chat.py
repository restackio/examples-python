import os

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel
from restack_ai.function import FunctionFailure, function, log

load_dotenv()

def raise_missing_api_key_error() -> None:
    error_message = "OPENAI_API_KEY is not set"
    log.error(error_message)
    raise FunctionFailure(error_message, non_retryable=True)


class OpenAiChatInput(BaseModel):
    user_content: str
    system_content: str | None = None
    model: str | None = None


@function.defn()
async def openai_chat(openai_chat_input: OpenAiChatInput) -> str:
    try:
        log.info("openai_chat function started", input=openai_chat_input)

        if os.environ.get("OPENAI_API_KEY") is None:
            raise_missing_api_key_error()

        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        messages = []
        if input.system_content:
            messages.append({"role": "system", "content": input.system_content})
        messages.append({"role": "user", "content": input.user_content})

        response = client.chat.completions.create(
            model=input.model or "gpt-4o-mini",
            messages=messages,
        )
        log.info("openai_chat function completed", response=response)
        return response.choices[0].message.content
    except Exception as e:
        error_message = "Failed to chat with OpenAI"
        log.error(error_message, error=e)
        raise FunctionFailure(error_message, non_retryable=True) from e
