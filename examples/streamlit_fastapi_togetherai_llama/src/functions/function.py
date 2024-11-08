from llama_index.llms.together import TogetherLLM
from restack_ai.function import function, log, FunctionFailure
from llama_index.core.llms import ChatMessage, MessageRole
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class FunctionInputParams:
    prompt: str

@function.defn(name="llm_complete")
async def llm_complete(input: FunctionInputParams):
    try:
        api_key = os.getenv("TOGETHER_API_KEY")
        if not api_key:
            log.error("TOGETHER_API_KEY environment variable is not set.")
            raise ValueError("TOGETHER_API_KEY environment variable is required.")
    
        llm = TogetherLLM(
            model="mistralai/Mixtral-8x7B-Instruct-v0.1", api_key=api_key
        )
        messages = [
            ChatMessage(
                # This is a system prompt that is used to set the behavior of the LLM. You can update this llm_complete function to also accept a system prompt as an input parameter.
                role=MessageRole.SYSTEM, content="You are a pirate with a colorful personality"
            ),
            ChatMessage(role=MessageRole.USER, content=input.prompt),
        ]
        resp = llm.chat(messages)
        return resp.message.content
    except Exception as e:
        log.error(f"Error interacting with llm: {e}")
        raise FunctionFailure(f"Error interacting with llm: {e}", non_retryable=True)
  