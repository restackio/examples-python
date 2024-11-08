from restack_ai.function import function, log
from dataclasses import dataclass
import google.generativeai as genai
import os

@dataclass
class FunctionInputParams:
    user_content: str

@function.defn(name="GeminiGenerate")
async def gemini_generate(input: FunctionInputParams) -> str:
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash")

    response = model.generate_content(input.user_content)
    return response.text
