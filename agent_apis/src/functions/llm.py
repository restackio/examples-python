import os
from dataclasses import dataclass

from dotenv import load_dotenv
from openai import OpenAI
from restack_ai.function import NonRetryableError, function, log

load_dotenv()


@dataclass
class FunctionInputParams:
    user_content: str
    system_content: str | None = None
    model: str | None = None


def raise_exception(message: str) -> None:
    log.error(message)
    raise Exception(message)


@function.defn()
async def llm(function_input: FunctionInputParams) -> str:
    try:
        log.info("llm function started", input=function_input)

        if os.environ.get("RESTACK_API_KEY") is None:
            error_message = "RESTACK_API_KEY is not set"
            raise_exception(error_message)

        client = OpenAI(
            base_url="https://ai.restack.io", api_key=os.environ.get("RESTACK_API_KEY")
        )

        messages = []
        if function_input.system_content:
            messages.append(
                {"role": "system", "content": function_input.system_content}
            )
        messages.append({"role": "user", "content": function_input.user_content})

        response = client.chat.completions.create(
            model=function_input.model or "gpt-4o-mini", messages=messages
        )
        log.info("llm function completed", response=response)
        return response.choices[0].message.content
    except Exception as e:
        error_message = "llm function failed"
        raise NonRetryableError(error_message) from e
