from llama_index.llms.together import TogetherLLM
from restack_ai.function import function, log, FunctionFailure
from llama_index.core.llms import ChatMessage, MessageRole
import os
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class FunctionInputParams(BaseModel):
    prompt: str

@function.defn(name="llm_complete")
async def llm_complete(input: FunctionInputParams):
    try:
        llm = TogetherLLM(
            model="mistralai/Mixtral-8x7B-Instruct-v0.1", api_key=os.getenv("TOGETHER_API_KEY")
        )
        messages = [
            ChatMessage(
                role=MessageRole.SYSTEM, content="You are a pirate with a colorful personality"
            ),
            ChatMessage(role=MessageRole.USER, content=input.prompt),
        ]
        resp = llm.chat(messages)
        return resp.message.content
    except Exception as e:
        log.error(f"Error interacting with llm: {e}")
        raise FunctionFailure(f"Error interacting with llm: {e}", non_retryable=True)
  