from restack_ai.function import function
from pydantic import BaseModel
from restack_google_gemini import gemini_generate_content, GeminiGenerateContentInput
import os

class FunctionInputParams(BaseModel):
    user_content: str

@function.defn(name="GeminiGenerateOpposite")
async def gemini_generate_opposite(input: FunctionInputParams) -> str:
    response = gemini_generate_content(
        GeminiGenerateContentInput(
            user_content=input.user_content,
            model="gemini-1.5-flash",
            api_key=os.environ.get("GEMINI_API_KEY"),
        )
    )
    return response
