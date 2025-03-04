import os
from typing import Literal

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel
from restack_ai.function import NonRetryableError, function, log

load_dotenv()


class Message(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str


class LlmChatInput(BaseModel):
    system_content: str | None = None
    model: str | None = None
    messages: list[Message] | None = None


def raise_exception(message: str) -> None:
    log.error(message)
    raise NonRetryableError(message)


@function.defn()
async def llm_chat(agent_input: LlmChatInput) -> dict[str, str]:
    try:
        log.info("llm_chat function started", agent_input=agent_input)

        if os.environ.get("RESTACK_API_KEY") is None:
            error_message = "RESTACK_API_KEY is not set"
            raise_exception(error_message)

        client = OpenAI(
            base_url="https://ai.restack.io", api_key=os.environ.get("RESTACK_API_KEY")
        )

        if agent_input.system_content:
            agent_input.messages.append(
                {"role": "system", "content": agent_input.system_content}
            )

        assistant_raw_response = client.chat.completions.create(
            model=agent_input.model or "gpt-4o-mini",
            messages=agent_input.messages,
        )
    except Exception as e:
        error_message = f"LLM chat failed: {e}"
        raise NonRetryableError(error_message) from e
    else:
        log.info(
            "llm_chat function completed", assistant_raw_response=assistant_raw_response
        )

        assistant_response = {
            "role": assistant_raw_response.choices[0].message.role,
            "content": assistant_raw_response.choices[0].message.content,
        }

        log.info("assistant_response", assistant_response=assistant_response)

        return assistant_response
