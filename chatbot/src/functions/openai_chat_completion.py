from restack_ai.function import function, log
from openai import OpenAI
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

class OpenAIInputParams(BaseModel):
    user_content: str = "What is restack?"
    system_content: str | None = "You are a helpful assistant"
    model: str | None = "gpt-4o-mini"
    base_url: str | None = "https://ai.restack.io"

class OpenAIOutputParams(BaseModel):
    message: str

@function.defn()
async def openai_chat_completion(input: OpenAIInputParams) -> OpenAIOutputParams:
    try:
        log.info("openai_chat_completion function started", input=input)
        
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
            
        client = OpenAI(api_key=api_key, base_url=input.base_url)

        messages = []
        if input.system_content:
            messages.append({"role": "system", "content": input.system_content})
        messages.append({"role": "user", "content": input.user_content})

        response = client.chat.completions.create(
            model=input.model or "restack-r1",
            messages=messages,
        )
        log.info("openai_chat_completion function completed", response=response)
        return OpenAIOutputParams(message=response.choices[0].message.content)
    except Exception as e:
        log.error("openai_chat_completion function failed", error=e)
        raise e
