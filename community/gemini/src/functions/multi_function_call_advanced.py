from restack_ai.function import function, log
from pydantic import BaseModel
from google import genai
from google.genai import types
from typing import List, Optional

import os
from src.functions.tools import get_function_declarations

class ChatMessage(BaseModel):
    role: str
    content: str

class FunctionInputParams(BaseModel):
    user_content: str
    chat_history: Optional[List[ChatMessage]] = None

@function.defn()
async def gemini_multi_function_call_advanced(input: FunctionInputParams):
    try:
        log.info("gemini_multi_function_call_advanced function started", input=input)
        client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

        functions = get_function_declarations()
        tools = [types.Tool(function_declarations=functions)]

        response = client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents=[input.user_content] + ([msg.content for msg in input.chat_history] if input.chat_history else []),
            config=types.GenerateContentConfig(
                tools=tools
            )
        )
        return response
    
    except Exception as e:
        log.error("Error in gemini_multi_function_call_advanced", error=str(e))
        raise e