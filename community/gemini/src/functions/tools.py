from restack_ai.function import function, log
from pydantic import BaseModel, validator
from typing import List, Optional, Dict
import inspect

from enum import Enum

class USTopCities(str, Enum):
    NEW_YORK = "New York, NY"
    LOS_ANGELES = "Los Angeles, CA" 
    CHICAGO = "Chicago, IL"
    HOUSTON = "Houston, TX"
    PHOENIX = "Phoenix, AZ"
    PHILADELPHIA = "Philadelphia, PA"
    SAN_ANTONIO = "San Antonio, TX"
    SAN_DIEGO = "San Diego, CA"
    DALLAS = "Dallas, TX"
    SAN_JOSE = "San Jose, CA"
    AUSTIN = "Austin, TX"
    JACKSONVILLE = "Jacksonville, FL"
    FORT_WORTH = "Fort Worth, TX"
    COLUMBUS = "Columbus, OH"
    SAN_FRANCISCO = "San Francisco, CA"
    CHARLOTTE = "Charlotte, NC"
    INDIANAPOLIS = "Indianapolis, IN"
    SEATTLE = "Seattle, WA"
    DENVER = "Denver, CO"
    WASHINGTON_DC = "Washington, DC"
    BOSTON = "Boston, MA"
    EL_PASO = "El Paso, TX"
    DETROIT = "Detroit, MI"
    NASHVILLE = "Nashville, TN"
    PORTLAND = "Portland, OR"
    MEMPHIS = "Memphis, TN"
    OKLAHOMA_CITY = "Oklahoma City, OK"
    LAS_VEGAS = "Las Vegas, NV"
    LOUISVILLE = "Louisville, KY"
    BALTIMORE = "Baltimore, MD"
    MILWAUKEE = "Milwaukee, WI"
    ALBUQUERQUE = "Albuquerque, NM"
    TUCSON = "Tucson, AZ"
    FRESNO = "Fresno, CA"
    SACRAMENTO = "Sacramento, CA"
    MESA = "Mesa, AZ"
    KANSAS_CITY = "Kansas City, MO"
    ATLANTA = "Atlanta, GA"
    MIAMI = "Miami, FL"
    COLORADO_SPRINGS = "Colorado Springs, CO"
    RALEIGH = "Raleigh, NC"
    OMAHA = "Omaha, NE"
    LONG_BEACH = "Long Beach, CA"
    VIRGINIA_BEACH = "Virginia Beach, VA"
    OAKLAND = "Oakland, CA"
    MINNEAPOLIS = "Minneapolis, MN"
    TULSA = "Tulsa, OK"
    ARLINGTON = "Arlington, TX"
    TAMPA = "Tampa, FL"
    NEW_ORLEANS = "New Orleans, LA"

class WeatherData(BaseModel):
    temperature: str
    humidity: str
    air_quality: str

class LocationInput(BaseModel):
    """The city and state, e.g. San Francisco, CA"""
    location: USTopCities

CITY_WEATHER_DATA: Dict[USTopCities, WeatherData] = {
    USTopCities.NEW_YORK: WeatherData(temperature="72°F", humidity="60%", air_quality="moderate"),
    USTopCities.LOS_ANGELES: WeatherData(temperature="75°F", humidity="65%", air_quality="good"),
    USTopCities.CHICAGO: WeatherData(temperature="68°F", humidity="55%", air_quality="good"), 
    USTopCities.HOUSTON: WeatherData(temperature="82°F", humidity="75%", air_quality="moderate"),
    USTopCities.PHOENIX: WeatherData(temperature="95°F", humidity="25%", air_quality="good"),
    USTopCities.PHILADELPHIA: WeatherData(temperature="70°F", humidity="62%", air_quality="moderate"),
    USTopCities.SAN_ANTONIO: WeatherData(temperature="85°F", humidity="70%", air_quality="good"),
    USTopCities.SAN_DIEGO: WeatherData(temperature="72°F", humidity="68%", air_quality="good"),
    USTopCities.DALLAS: WeatherData(temperature="83°F", humidity="65%", air_quality="moderate"),
    USTopCities.SAN_JOSE: WeatherData(temperature="73°F", humidity="60%", air_quality="good"),
    USTopCities.AUSTIN: WeatherData(temperature="84°F", humidity="68%", air_quality="good"),
    USTopCities.JACKSONVILLE: WeatherData(temperature="80°F", humidity="75%", air_quality="moderate"),
    USTopCities.FORT_WORTH: WeatherData(temperature="83°F", humidity="65%", air_quality="moderate"),
    USTopCities.COLUMBUS: WeatherData(temperature="71°F", humidity="63%", air_quality="good"),
    USTopCities.SAN_FRANCISCO: WeatherData(temperature="65°F", humidity="75%", air_quality="good"),
    USTopCities.CHARLOTTE: WeatherData(temperature="76°F", humidity="65%", air_quality="good"),
    USTopCities.INDIANAPOLIS: WeatherData(temperature="72°F", humidity="64%", air_quality="moderate"),
    USTopCities.SEATTLE: WeatherData(temperature="62°F", humidity="80%", air_quality="good"),
    USTopCities.DENVER: WeatherData(temperature="70°F", humidity="45%", air_quality="good"),
    USTopCities.WASHINGTON_DC: WeatherData(temperature="74°F", humidity="65%", air_quality="moderate"),
    USTopCities.BOSTON: WeatherData(temperature="68°F", humidity="70%", air_quality="good"),
    USTopCities.EL_PASO: WeatherData(temperature="88°F", humidity="30%", air_quality="good"),
    USTopCities.DETROIT: WeatherData(temperature="69°F", humidity="65%", air_quality="moderate"),
    USTopCities.NASHVILLE: WeatherData(temperature="77°F", humidity="68%", air_quality="good"),
    USTopCities.PORTLAND: WeatherData(temperature="65°F", humidity="75%", air_quality="good"),
    USTopCities.MEMPHIS: WeatherData(temperature="79°F", humidity="70%", air_quality="moderate"),
    USTopCities.OKLAHOMA_CITY: WeatherData(temperature="80°F", humidity="60%", air_quality="good"),
    USTopCities.LAS_VEGAS: WeatherData(temperature="92°F", humidity="25%", air_quality="good"),
    USTopCities.LOUISVILLE: WeatherData(temperature="75°F", humidity="67%", air_quality="moderate"),
    USTopCities.BALTIMORE: WeatherData(temperature="73°F", humidity="65%", air_quality="moderate"),
    USTopCities.MILWAUKEE: WeatherData(temperature="65°F", humidity="70%", air_quality="good"),
    USTopCities.ALBUQUERQUE: WeatherData(temperature="82°F", humidity="35%", air_quality="good"),
    USTopCities.TUCSON: WeatherData(temperature="90°F", humidity="30%", air_quality="good"),
    USTopCities.FRESNO: WeatherData(temperature="85°F", humidity="45%", air_quality="moderate"),
    USTopCities.SACRAMENTO: WeatherData(temperature="80°F", humidity="55%", air_quality="moderate"),
    USTopCities.MESA: WeatherData(temperature="93°F", humidity="25%", air_quality="good"),
    USTopCities.KANSAS_CITY: WeatherData(temperature="75°F", humidity="65%", air_quality="good"),
    USTopCities.ATLANTA: WeatherData(temperature="78°F", humidity="70%", air_quality="moderate"),
    USTopCities.MIAMI: WeatherData(temperature="85°F", humidity="80%", air_quality="moderate"),
    USTopCities.COLORADO_SPRINGS: WeatherData(temperature="68°F", humidity="45%", air_quality="good"),
    USTopCities.RALEIGH: WeatherData(temperature="75°F", humidity="68%", air_quality="good"),
    USTopCities.OMAHA: WeatherData(temperature="73°F", humidity="65%", air_quality="good"),
    USTopCities.LONG_BEACH: WeatherData(temperature="74°F", humidity="70%", air_quality="moderate"),
    USTopCities.VIRGINIA_BEACH: WeatherData(temperature="76°F", humidity="75%", air_quality="good"),
    USTopCities.OAKLAND: WeatherData(temperature="68°F", humidity="75%", air_quality="good"),
    USTopCities.MINNEAPOLIS: WeatherData(temperature="65°F", humidity="65%", air_quality="good"),
    USTopCities.TULSA: WeatherData(temperature="78°F", humidity="65%", air_quality="good"),
    USTopCities.ARLINGTON: WeatherData(temperature="83°F", humidity="65%", air_quality="moderate"),
    USTopCities.TAMPA: WeatherData(temperature="83°F", humidity="75%", air_quality="moderate"),
    USTopCities.NEW_ORLEANS: WeatherData(temperature="82°F", humidity="80%", air_quality="moderate")
}

@function.defn()
async def get_current_temperature(input: LocationInput) -> str:
    description = "Get the current temperature for a specific location"
    log.info("get_current_temperature function started", location=input.location)
    weather_data = CITY_WEATHER_DATA.get(input.location, WeatherData(temperature="75°F", humidity="65%", air_quality="good"))
    return weather_data.temperature

@function.defn()
async def get_humidity(input: LocationInput) -> str:
    description = "Get the current humidity level for a specific location"
    log.info("get_humidity function started", location=input.location)
    weather_data = CITY_WEATHER_DATA.get(input.location, WeatherData(temperature="75°F", humidity="65%", air_quality="good"))
    return weather_data.humidity

@function.defn()
async def get_air_quality(input: LocationInput) -> str:
    description = "Get the current air quality for a specific location"
    log.info("get_air_quality function started", location=input.location)
    weather_data = CITY_WEATHER_DATA.get(input.location, WeatherData(temperature="75°F", humidity="65%", air_quality="good"))
    return weather_data.air_quality

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
                    "location": {
                        "type": "STRING",
                        "description": input_type.__doc__,
                        "enum": [city.value for city in USTopCities]
                    }
                },
                "required": ["location"]
            }
        })
    return functions