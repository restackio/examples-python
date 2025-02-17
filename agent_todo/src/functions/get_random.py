import secrets

from pydantic import BaseModel
from restack_ai.function import function, log


class RandomParams(BaseModel):
    todo_title: str


@function.defn()
async def get_random(params: RandomParams) -> str:
    try:
        random_number = secrets.randbelow(100)
    except Exception as e:
        log.error("random function failed", error=e)
        raise
    else:
        return f"The random number for {params.todo_title} is {random_number}."
