from restack_ai.function import function
from pydantic import BaseModel
from openai import OpenAI
import os

class FunctionInputParams(BaseModel):
    user_content: str
    message_schema: dict

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@function.defn(name="OpenaiGreet")
async def openai_greet(input: FunctionInputParams) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": input.user_content}],
        response_format={"type": "json_schema"},
        functions=[input.message_schema],
        function_call={"name": input.message_schema["name"]}
    )
    return response