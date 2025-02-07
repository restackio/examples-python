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


@function.defn()
async def llm_complete(llm_complete_input: FunctionInputParams) -> str:
    try:
        log.info("llm_complete function started", input=llm_complete_input)
        llm = TogetherLLM(
            model="meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo",
            api_key=os.getenv("TOGETHER_API_KEY"),
        )
        messages = [
            ChatMessage(
                # This is a system prompt that is used to set the behavior of the LLM.
                # You can update this llm_complete function
                # to also accept a system prompt as an input parameter.
                role=MessageRole.SYSTEM,
                content="You are a pirate with a colorful personality",
            ),
            ChatMessage(role=MessageRole.USER, content=llm_complete_input.prompt),
        ]
        resp = llm.chat(messages)
    except Exception as e:
        error_message = "Error interacting with llm"
        log.error(error_message, error=e)
        raise FunctionFailure(error_message) from e
    else:
        log.info("llm_complete function completed", response=resp.message.content)
        return resp.message.content
