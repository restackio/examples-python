from restack_ai.function import function, log
from dataclasses import dataclass
import google.generativeai as genai
import os

@dataclass
class FunctionInputParams:
    user_content: str

@function.defn()
async def gemini_generate(input: FunctionInputParams) -> str:
    try:
        log.info("gemini_generate function started", input=input)
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
        model = genai.GenerativeModel("gemini-1.5-flash")

        response = model.generate_content(input.user_content)
        log.info("gemini_generate function completed", response=response.text)
        return response.text
    except Exception as e:
        log.error("gemini_generate function failed", error=e)
        raise e
