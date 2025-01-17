from restack_ai.function import function, log
from pydantic import BaseModel
from typing import List, Optional
import inspect

class TemperatureInput(BaseModel):
    """The city and state, e.g. San Francisco, CA"""
    location: str

class HumidityInput(BaseModel):
    """The city and state, e.g. San Francisco, CA"""
    location: str

class AirQualityInput(BaseModel):
    """The city and state, e.g. San Francisco, CA"""
    location: str

@function.defn()
async def get_current_temperature(input: TemperatureInput) -> str:
    description = "Get the current temperature for a specific location"
    log.info("get_current_temperature function started", location=input.location)
    return '75°F'

@function.defn()
async def get_humidity(input: HumidityInput) -> str:
    description = "Get the current humidity level for a specific location"
    log.info("get_humidity function started", location=input.location)
    return '65%'

@function.defn()
async def get_air_quality(input: AirQualityInput) -> str:
    description = "Get the current air quality for a specific location"
    log.info("get_air_quality function started", location=input.location)
    return 'good'

def get_function_declarations():
    functions = []
    for func in [get_current_temperature, get_humidity, get_air_quality]:
        input_type = func.__annotations__['input']
        source = inspect.getsource(func)
        description = source.split('description = "')[1].split('"')[0]
        functions.append({
            "name": func.__name__,
            "description": description,
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    field_name: {
                        "type": "STRING",
                        "description": input_type.__doc__,
                    } for field_name in input_type.__fields__
                },
                "required": list(input_type.__fields__.keys())
            }
        })
    return functions