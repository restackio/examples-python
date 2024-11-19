from restack_ai.function import function, log
from pydantic import BaseModel
from restack_google_gemini import gemini_generate_content, GeminiGenerateContentInput
import os

class FunctionInputParams(BaseModel):
    user_content: str

@function.defn()
async def gemini_generate(input: FunctionInputParams) -> str:
    log.info(input)
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        log.error("GEMINI_API_KEY environment variable is not set.")
        raise ValueError("GEMINI_API_KEY environment variable is required.")
    response = gemini_generate_content(
        GeminiGenerateContentInput(
            user_content=input.user_content,
            model="gemini-1.5-flash",
            api_key=os.getenv("GEMINI_API_KEY"),
            generation_config={}
        )
    )
    log.info(response)
    return response
