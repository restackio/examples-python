import os
from dataclasses import dataclass

from dotenv import load_dotenv
from openai import OpenAI
from restack_ai.function import FunctionFailure, function, log

load_dotenv()


@dataclass
class FunctionInputParams:
    user_content: str
    system_content: str | None = None
    model: str | None = None


@function.defn()
async def openai_greet(openai_greet_input: FunctionInputParams) -> str:
    try:
        log.info("openai_greet function started", input=openai_greet_input)
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        messages = []
        if openai_greet_input.system_content:
            messages.append({
                "role": "system",
                "content": openai_greet_input.system_content,
            })
        messages.append({
            "role": "user",
            "content": openai_greet_input.user_content,
        })

        response = client.chat.completions.create(
            model=openai_greet_input.model or "gpt-4o-mini",
            messages=messages,
            response_format={
                "json_schema": {
                    "name": "greet",
                    "description": "Greet a person",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "message": {"type": "string"},
                        },
                        "required": ["message"],
                    },
                },
                "type": "json_schema",
            },
        )
        log.info("openai_greet function completed", response=response)
        return response.choices[0].message.content
    except Exception as e:
        error_message = "Failed to greet with OpenAI"
        log.error(error_message, error=e)
        raise FunctionFailure(error_message, non_retryable=True) from e
