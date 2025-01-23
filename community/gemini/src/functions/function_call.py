from restack_ai.function import function, log
from pydantic import BaseModel
from google import genai
from google.genai import types

import os

@function.defn()
def get_current_weather(location: str) -> str:
    """Returns the current weather.

    Args:
        location: The city and state, e.g. San Francisco, CA
    """
    log.info("get_current_weather function started", location=location)
    return 'sunny'

class FunctionInputParams(BaseModel):
    user_content: str

@function.defn()
async def gemini_function_call(input: FunctionInputParams) -> str:
    try:
        log.info("gemini_function_call function started", input=input)
        client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
        
        response = client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents=input.user_content,
            config=types.GenerateContentConfig(tools=[get_current_weather])
        )
        log.info("gemini_function_call function completed", response=response.text)
        return response.text
    except Exception as e:
        log.error("gemini_function_call function failed", error=e)
        raise e
