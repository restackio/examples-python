import os

from google import genai
from google.genai import types
from pydantic import BaseModel
from restack_ai.function import FunctionFailure, function, log

from src.functions.tools import get_function_declarations


class ChatMessage(BaseModel):
    role: str
    content: str


class FunctionInputParams(BaseModel):
    user_content: str
    chat_history: list[ChatMessage] | None = None


@function.defn()
async def gemini_multi_function_call_advanced(
    gmfca_input: FunctionInputParams,
) -> str:
    try:
        log.info(
            "gemini_multi_function_call_advanced function started",
            input=gmfca_input,
        )
        client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

        functions = get_function_declarations()
        tools = [types.Tool(function_declarations=functions)]

        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=[
                gmfca_input.user_content,
            ]
            + (
                [msg.content for msg in gmfca_input.chat_history]
                if gmfca_input.chat_history
                else []
            ),
            config=types.GenerateContentConfig(
                tools=tools,
            ),
        )
    except Exception as e:
        error_message = "Error in gemini_multi_function_call_advanced"
        log.error(error_message, error=e)
        raise FunctionFailure(error_message) from e
    else:
        return response
