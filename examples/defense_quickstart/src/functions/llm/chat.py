from restack_ai.function import function, log
from openai import OpenAI
from dataclasses import dataclass
import os

@dataclass
class ResponseFormat:
    name: str
    description: str
    schema: dict

@dataclass
class FunctionInputParams:
    system_prompt: str
    user_prompt: str | None = None
    model: str | None = None

@function.defn()
async def llm_chat(input: FunctionInputParams) -> str:
    try:
        log.info("llm_chat function started", input=input)
        client = OpenAI(base_url=os.environ.get("OPENBABYLON_API_URL"))

        messages = []
        if input.system_prompt:
            messages.append({"role": "system", "content": input.system_prompt})
        messages.append({"role": "user", "content": input.user_prompt})

        response = client.chat.completions.create(
            model="orpo-mistral-v0.3-ua-tokV2-focus-10B-low-lr-1epoch-aux-merged-1ep",
            messages=messages,
        )
        log.info("openai_greet function completed", response=response)
        return response.choices[0].message.content
    except Exception as e:
        log.error("openai_greet function failed", error=e)
        raise e
