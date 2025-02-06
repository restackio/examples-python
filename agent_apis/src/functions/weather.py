from restack_ai.function import function, log
import aiohttp

@function.defn()
async def weather() -> str:
    url = f"https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    try:
      async with aiohttp.ClientSession() as session:
          async with session.get(url) as response:
              log.info("response", response=response)
              if response.status == 200:
                  data = await response.json()
                  log.info("weather data", data=data)
                  return str(data)
              else:
                  log.error("Error: {response}")
                  raise Exception(f"Error: {response.status}")
    except Exception as e:
        log.error("Error: {e}")
        raise e
    