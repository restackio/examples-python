import os
from dataclasses import dataclass

from dotenv import load_dotenv
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.llms.together import TogetherLLM
from restack_ai.function import FunctionFailure, function, log

load_dotenv()


@dataclass
class FunctionInputParams:
    prompt: str

def raise_together_api_key_error() -> None:
    error_message = "TOGETHER_API_KEY environment variable is not set."
    log.error(error_message)
    raise ValueError(error_message)


@function.defn()
async def llm_complete(function_input: FunctionInputParams) -> str:
    try:
        log.info("llm_complete function started", input=function_input)
        api_key = os.getenv("TOGETHER_API_KEY")
        if not api_key:
            raise_together_api_key_error()

        llm = TogetherLLM(
            model="meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo",
            api_key=api_key,
        )
        messages = [
            ChatMessage(
                role=MessageRole.SYSTEM,
                content="You are a pirate with a colorful personality",
            ),
            ChatMessage(role=MessageRole.USER, content=function_input.prompt),
        ]
        resp = llm.chat(messages)
    except Exception as e:
        error_message = "llm_complete function failed"
        log.error(error_message, error=e)
        raise FunctionFailure(error_message, non_retryable=True) from e
    else:
        log.info("llm_complete function completed", response=resp.message.content)
        return resp.message.content
