import aiohttp
from restack_ai.function import NonRetryableError, function, log

HTTP_OK = 200


def raise_exception(message: str) -> None:
    log.error(message)
    raise Exception(message)


@function.defn()
async def weather() -> str:
    url = "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    try:
        async with aiohttp.ClientSession() as session, session.get(url) as response:
            log.info("response", response=response)
            if response.status == HTTP_OK:
                data = await response.json()
                log.info("weather data", data=data)
                return str(data)
            error_message = f"Error: {response.status}"
            raise_exception(error_message)
    except Exception as e:
        error_message = f"Error: {e}"
        raise NonRetryableError(error_message) from e
