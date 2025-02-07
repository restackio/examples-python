import os

from dotenv import load_dotenv
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.llms.together import TogetherLLM
from pydantic import BaseModel
from restack_ai.function import FunctionFailure, function, log

load_dotenv()


class FunctionInputParams(BaseModel):
    system_prompt: str
    user_prompt: str

def environment_variable_error(variable_name: str) -> FunctionFailure:
    error_message = f"{variable_name} environment variable is not set."
    log.error(error_message)
    raise FunctionFailure(error_message, non_retryable=True)


@function.defn()
async def llm_chat(llm_chat_input: FunctionInputParams) -> str:
    try:
        api_key = os.getenv("TOGETHER_API_KEY")
        if not api_key:
            environment_variable_error("TOGETHER_API_KEY")

        llm = TogetherLLM(
            model="meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo",
            api_key=api_key,
        )
        messages = [
            ChatMessage(
                role=MessageRole.SYSTEM,
                content=llm_chat_input.system_prompt,
            ),
            ChatMessage(
                role=MessageRole.USER,
                content=llm_chat_input.user_prompt,
            ),
        ]
        resp = llm.chat(messages)
    except Exception as e:
        error_message = "Error interacting with llm"
        log.error(error_message, error=e)
        raise FunctionFailure(error_message, non_retryable=True) from e
    else:
        return resp.message.content
