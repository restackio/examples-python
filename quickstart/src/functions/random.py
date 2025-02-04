from restack_ai.function import function, log
from pydantic import BaseModel
import random

class RandomParams(BaseModel):
    todoTile: str

@function.defn()
async def get_random(params: RandomParams) -> str:
    try:
        random_number = random.randint(0, 100)
        return f"The random number for {params.todoTile} is {random_number}."
    except Exception as e:
        log.error("random function failed", error=e)
        raise e
