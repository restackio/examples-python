from restack_ai.function import function, log
from pydantic import BaseModel
from google import genai
from google.genai import types
from typing import List, Optional

import os

class ChatMessage(BaseModel):
    role: str
    content: str

class FunctionInputParams(BaseModel):
    user_content: str
    chat_history: Optional[List[ChatMessage]] = None

class WeatherInput(BaseModel):
    location: str

class HumidityInput(BaseModel):
    location: str

class AirQualityInput(BaseModel):
    location: str

@function.defn()
async def get_current_weather(input: WeatherInput) -> str:
    log.info("get_current_weather function started", location=input.location)
    return 'sunny'

@function.defn()
async def get_humidity(input: HumidityInput) -> str:
    log.info("get_humidity function started", location=input.location)
    return '65%'

@function.defn()
async def get_air_quality(input: AirQualityInput) -> str:
    log.info("get_air_quality function started", location=input.location)
    return 'good'

@function.defn()
async def gemini_multi_function_call_advanced(input: FunctionInputParams) :
    try:
        log.info("gemini_multi_function_call_advanced function started", input=input)
        client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

        functions = [
            {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "OBJECT",
                    "properties": {
                        "location": {
                            "type": "STRING",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                    },
                    "required": ["location"],
                }
            },
            {
                "name": "get_humidity", 
                "description": "Get the current humidity in a given location",
                "parameters": {
                    "type": "OBJECT",
                    "properties": {
                        "location": {
                            "type": "STRING",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                    },
                    "required": ["location"],
                }
            },
            {
                "name": "get_air_quality",
                "description": "Get the current air quality in a given location", 
                "parameters": {
                    "type": "OBJECT",
                    "properties": {
                        "location": {
                            "type": "STRING",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                    },
                    "required": ["location"],
                }
            }
        ]

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