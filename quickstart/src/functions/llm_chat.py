from restack_ai.function import function, log
from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Literal, Optional, List

load_dotenv()

class Message(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str

class LlmChatInput(BaseModel):
    system_content: Optional[str] = None
    model: Optional[str] = None
    messages: Optional[List[Message]] = None

@function.defn()
async def llm_chat(input: LlmChatInput) -> ChatCompletion:
    try:
        log.info("llm_chat function started", input=input)
        client = OpenAI(base_url="https://ai.restack.io", api_key=os.environ.get("RESTACK_API_KEY"))


        if input.system_content:
            input.messages.append({"role": "system", "content": input.system_content})

        response = client.chat.completions.create(
            model=input.model or "restack-c1",
            messages=input.messages,
        )
        log.info("llm_chat function completed", response=response)

        return response
    except Exception as e:
        log.error("llm_chat function failed", error=e)
        raise e
