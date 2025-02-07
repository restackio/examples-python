import os
from dataclasses import dataclass

import google.generativeai as genai
from restack_ai.function import FunctionFailure, function, log


@dataclass
class FunctionInputParams:
    user_content: str


@function.defn()
async def gemini_generate(gemini_generate_input: FunctionInputParams) -> str:
    try:
        log.info("gemini_generate function started", input=gemini_generate_input)
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
        model = genai.GenerativeModel("gemini-1.5-flash")

        response = model.generate_content(gemini_generate_input.user_content)
    except Exception as e:
        error_message = "gemini_generate function failed"
        log.error(error_message, error=e)
        raise FunctionFailure(error_message) from e
    else:
        log.info("gemini_generate function completed", response=response.text)
        return response.text
