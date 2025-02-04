from restack_ai.function import function, log
from pydantic import BaseModel
import random


class RandomParams(BaseModel):
    todoTitle: str


@function.defn()
async def get_random(params: RandomParams) -> str:
    try:
        random_number = random.randint(0, 100)
        return f"The random number for {params.todoTitle} is {random_number}."
    except Exception as e:
        log.error("random function failed", error=e)
        raise e
