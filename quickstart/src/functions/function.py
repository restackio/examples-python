from restack_ai.function import function, log
from pydantic import BaseModel

class WelcomeInput(BaseModel):
    name: str

@function.defn()
async def welcome(input: WelcomeInput) -> str:
    try:
        log.info("welcome function started", input=input)
        return f"Hello, {input.name}!"
    except Exception as e:
        log.error("welcome function failed", error=e)
        raise e
