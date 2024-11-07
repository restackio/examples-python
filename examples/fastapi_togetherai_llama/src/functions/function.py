from llama_index.llms.together import TogetherLLM
from restack_ai.function import function, log, FunctionFailure
import os
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class FunctionInputParams(BaseModel):
    prompt: str

@function.defn(name="llm_complete")
async def llm_complete(input: FunctionInputParams) -> str:
    try:
        llm = TogetherLLM(
            model="mistralai/Mixtral-8x7B-Instruct-v0.1", api_key=os.getenv("TOGETHER_API_KEY")
        )
        resp = llm.complete(input.prompt)
        return resp.text
    except Exception as e:
        log.error(f"Error interacting with llm: {e}")
        raise FunctionFailure(f"Error interacting with llm: {e}", non_retryable=True)
  