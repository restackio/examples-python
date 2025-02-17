from restack_ai.function import function, log, FunctionFailure
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
async def llm_chat(agent_input: LlmChatInput) -> ChatCompletion:
    try:
        log.info("llm_chat function started", agent_input=agent_input)

        if (os.environ.get("RESTACK_API_KEY") is None):
            raise FunctionFailure("RESTACK_API_KEY is not set", non_retryable=True)
        
        client = OpenAI(
            base_url="https://ai.restack.io", api_key=os.environ.get("RESTACK_API_KEY")
        )

        if agent_input.system_content:
            agent_input.messages.append({"role": "system", "content": agent_input.system_content})

        response = client.chat.completions.create(
            model=agent_input.model or "gpt-4o-mini",
            messages=agent_input.messages,
        )
        log.info("llm_chat function completed", response=response)

        return response
    except Exception as e:
        log.error("llm_chat function failed", error=e)
        raise e
