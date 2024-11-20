from llama_index.llms.together import TogetherLLM
from restack_ai.function import function, log, FunctionFailure, log
from llama_index.core.llms import ChatMessage, MessageRole
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class FunctionInputParams:
    prompt: str

@function.defn()
async def llm_complete(input: FunctionInputParams):
    try:
        log.info("llm_complete function started", input=input)
        api_key = os.getenv("TOGETHER_API_KEY")
        if not api_key:
            log.error("TOGETHER_API_KEY environment variable is not set.")
            raise ValueError("TOGETHER_API_KEY environment variable is required.")
    
        llm = TogetherLLM(
            model="meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo", api_key=api_key
        )
        messages = [
            ChatMessage(
                # This is a system prompt that is used to set the behavior of the LLM. You can update this llm_complete function to also accept a system prompt as an input parameter.
                role=MessageRole.SYSTEM, content="You are a pirate with a colorful personality"
            ),
            ChatMessage(role=MessageRole.USER, content=input.prompt),
        ]
        resp = llm.chat(messages)
        log.info("llm_complete function completed", response=resp.message.content)
        return resp.message.content
    except Exception as e:
        log.error("llm_complete function failed", error=e)
        raise e
  