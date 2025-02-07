import os
from dataclasses import dataclass

from openai import OpenAI
from restack_ai.function import FunctionFailure, function, log


@dataclass
class ResponseFormat:
    name: str
    description: str
    schema: dict


@dataclass
class FunctionInputParams:
    user_prompt: str
    model: str | None = None


@function.defn()
async def llm_chat(llm_chat_input: FunctionInputParams) -> str:
    try:
        log.info("llm_chat function started", llm_chat_input=llm_chat_input)

        openbabylon_url = os.environ.get("OPENBABYLON_API_URL")
        log.info("openbabylon_url", openbabylon_url=openbabylon_url)

        client = OpenAI(
            api_key="openbabylon",
            base_url=os.environ.get("OPENBABYLON_API_URL"),
        )

        messages = []
        if llm_chat_input.user_prompt:
            messages.append({"role": "user", "content": llm_chat_input.user_prompt})

        response = client.chat.completions.create(
            model="orpo-mistral-v0.3-ua-tokV2-focus-10B-low-lr-1epoch-aux-merged-1ep",
            messages=messages,
        )
    except Exception as e:
        error_message = "llm_chat function failed"
        log.error(error_message, error=e)
        raise FunctionFailure(error_message, non_retryable=True) from e
    else:
        log.info("llm_chat function completed", response=response)
        return response.choices[0].message.content
