import os
from restack_ai.function import function, log
from llama_index.llms.together import TogetherLLM

@function.defn(name="llm_complete")
async def llm_complete(prompt) -> str:
    try:
        log.info("llm_complete function started", prompt=prompt)
        llm = TogetherLLM(
            model="meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo", api_key=os.environ["TOGETHER_API_KEY"]
        )

        resp = llm.complete(prompt)

        log.info("llm_complete function completed", response=resp.text)

        return resp.text
    except Exception as e:
        log.error(f"Error seeding database: {e}")
        raise e
    