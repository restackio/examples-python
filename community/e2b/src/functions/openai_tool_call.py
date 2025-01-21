from restack_ai.function import function, log
from pydantic import BaseModel
import os
from openai import OpenAI

class OpenaiToolCallInput(BaseModel):
    user_content: str | None = None
    system_content: str | None = None
    tools: list[dict] = []
    model: str = "gpt-4"
    messages: list[dict] = []

@function.defn()
async def openai_tool_call(input: OpenaiToolCallInput) -> dict:
    try:
        log.info("openai_tool_call function started", input=input)
        
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        messages = input.messages.copy() if input.messages else [
            {"role": "system", "content": input.system_content}
        ]
        
        if input.user_content:
            messages.append({"role": "user", "content": input.user_content})

        response = client.chat.completions.create(
            model=input.model,
            messages=messages,
            **({"tools": input.tools} if input.tools else {})
        )

        response_message = response.choices[0].message
        messages.append(response_message)

        return {
            "messages": messages,
            "response": response_message
        }

    except Exception as e:
        log.error("openai_tool_call function failed", error=e)
        raise e
