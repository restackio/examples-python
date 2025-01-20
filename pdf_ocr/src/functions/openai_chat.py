from pydantic import BaseModel
from restack_ai.function import function, log, FunctionFailure
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

class OpenAiChatInput(BaseModel):
    user_content: str
    system_content: str | None = None
    model: str | None = None

@function.defn()
async def openai_chat(input: OpenAiChatInput) -> str:
    try:
        log.info("openai_chat function started", input=input)

        
        if (os.environ.get("OPENAI_API_KEY") is None):
            raise FunctionFailure("OPENAI_API_KEY is not set", non_retryable=True)
    
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        messages = []
        if input.system_content:
            messages.append({"role": "system", "content": input.system_content})
        messages.append({"role": "user", "content": input.user_content})

        response = client.chat.completions.create(
            model=input.model or "gpt-4o-mini",
            messages=messages
        )
        log.info("openai_chat function completed", response=response)
        return response.choices[0].message.content
    except Exception as e:
        log.error("openai_chat function failed", error=e)
        raise e
