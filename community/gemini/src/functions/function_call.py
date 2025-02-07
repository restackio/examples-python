import os

from google import genai
from google.genai import types
from pydantic import BaseModel
from restack_ai.function import FunctionFailure, function, log


@function.defn()
def get_current_weather(location: str) -> str:
    """Return the current weather.

    Args:
        location: The city and state, e.g. San Francisco, CA

    """
    log.info("get_current_weather function started", location=location)
    return "sunny"


class FunctionInputParams(BaseModel):
    user_content: str


@function.defn()
async def gemini_function_call(
    gemini_function_call_input: FunctionInputParams,
) -> str:
    try:
        log.info(
            "gemini_function_call function started",
            input=gemini_function_call_input,
        )
        client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=gemini_function_call_input.user_content,
            config=types.GenerateContentConfig(tools=[get_current_weather]),
        )
        log.info(
            "gemini_function_call function completed",
            response=response.text,
        )
        return response.text
    except Exception as e:
        error_message = "gemini_function_call function failed"
        log.error(error_message, error=e)
        raise FunctionFailure(error_message) from e
    else:
        return response.text
