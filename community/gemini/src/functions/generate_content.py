import os

from google import genai
from pydantic import BaseModel
from restack_ai.function import FunctionFailure, function, log


class FunctionInputParams(BaseModel):
    user_content: str


@function.defn()
async def gemini_generate_content(
    gemini_generate_content_input: FunctionInputParams,
) -> str:
    try:
        log.info(
            "gemini_generate_content function started",
            input=gemini_generate_content_input,
        )
        client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=gemini_generate_content_input.user_content,
        )
        log.info(
            "gemini_generate_content function completed",
            response=response.text,
        )
    except Exception as e:
        error_message = "gemini_generate_content function failed"
        log.error(error_message, error=e)
        raise FunctionFailure(error_message) from e
    else:
        return response.text
