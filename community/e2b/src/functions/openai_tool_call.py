import os

from openai import OpenAI
from pydantic import BaseModel
from restack_ai.function import FunctionFailure, function, log


class OpenaiToolCallInput(BaseModel):
    user_content: str | None = None
    system_content: str | None = None
    tools: list[dict] = []
    model: str = "gpt-4"
    messages: list[dict] = []


@function.defn()
async def openai_tool_call(otc_input: OpenaiToolCallInput) -> dict:
    try:
        log.info("openai_tool_call function started", otc_input=otc_input)

        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        messages = (
            otc_input.messages.copy()
            if otc_input.messages
            else [
                {"role": "system", "content": otc_input.system_content},
            ]
        )

        if otc_input.user_content:
            messages.append({"role": "user", "content": otc_input.user_content})

        response = client.chat.completions.create(
            model=otc_input.model,
            messages=messages,
            **({"tools": otc_input.tools} if otc_input.tools else {}),
        )

        response_message = response.choices[0].message
        messages.append(response_message)
    except Exception as e:
        error_message = "openai_tool_call function failed"
        log.error(error_message, error=e)
        raise FunctionFailure(error_message, non_retryable=True) from e
    else:
        log.info("openai_tool_call function succeeded")
        return {
            "messages": messages,
            "response": response_message,
        }
