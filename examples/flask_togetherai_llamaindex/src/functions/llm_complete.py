import os
from restack_ai.function import function, log
from llama_index.llms.together import TogetherLLM

@function.defn(name="llm_complete")
async def llm_complete() -> str:
    try:
        llm = TogetherLLM(
            model="mistralai/Mixtral-8x7B-Instruct-v0.1", api_key=os.environ["TOGETHER_API_KEY"]
        )

        resp = llm.complete("Who is Paul Graham?")

        log.info(resp.text)

        return resp.text
    except Exception as e:
        log.error(f"Error seeding database: {e}")
        raise e
    