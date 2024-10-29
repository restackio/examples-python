from restack_ai.function import function
from pydantic import BaseModel
from restack_integrations_openai import openai_chat_completion_base, OpenAIChatInput
import os

class FunctionInputParams(BaseModel):
    user_content: str
    message_schema: dict

@function.defn(name="OpenaiGreet")
async def openai_greet(input: FunctionInputParams) -> str:
    response = openai_chat_completion_base(
        OpenAIChatInput(
            user_content=input.user_content,
            model="gpt-4o-mini",
            json_schema=input.message_schema,
            api_key=os.environ.get("OPENAI_API_KEY"),
        )
    )
    return response.result.choices[0].message.content
