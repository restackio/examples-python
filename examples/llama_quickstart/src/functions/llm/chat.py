from llama_index.llms.together import TogetherLLM
from restack_ai.function import function, log, FunctionFailure
from llama_index.core.llms import ChatMessage, MessageRole
import os
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class FunctionInputParams(BaseModel):
    system_prompt: str
    user_prompt: str

@function.defn()
async def llm_chat(input: FunctionInputParams):
    try:
        api_key = os.getenv("TOGETHER_API_KEY")
        if not api_key:
            log.error("TOGETHER_API_KEY environment variable is not set.")
            raise ValueError("TOGETHER_API_KEY environment variable is required.")
    
        llm = TogetherLLM(
            model="meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo", api_key=api_key
        )
        messages = [
            ChatMessage(
                role=MessageRole.SYSTEM, content=input.system_prompt
            ),
            ChatMessage(
                role=MessageRole.USER, content=input.user_prompt
            ),
        ]
        resp = llm.chat(messages)
        return resp.message.content
    except Exception as e:
        log.error(f"Error interacting with llm: {e}")
        raise FunctionFailure(f"Error interacting with llm: {e}", non_retryable=True)
  