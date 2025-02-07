import os

from llama_index.llms.together import TogetherLLM
from restack_ai.function import FunctionFailure, function, log


@function.defn()
async def llm_complete(prompt: str) -> str:
    try:
        log.info("llm_complete function started", prompt=prompt)
        llm = TogetherLLM(
            model="meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo",
            api_key=os.environ["TOGETHER_API_KEY"],
        )

        resp = llm.complete(prompt)
    except Exception as e:
        error_message = "llm_complete function failed"
        log.error(error_message, error=e)
        raise FunctionFailure(error_message) from e
    else:
        log.info("llm_complete function completed", response=resp.text)
        return resp.text
