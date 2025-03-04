import secrets

from pydantic import BaseModel
from restack_ai.function import NonRetryableError, function


class RandomParams(BaseModel):
    todo_title: str


@function.defn()
async def get_random(params: RandomParams) -> str:
    try:
        random_number = secrets.randbelow(100)
    except Exception as e:
        error_message = f"get_random function failed: {e}"
        raise NonRetryableError(error_message) from e
    else:
        return f"The random number for {params.todo_title} is {random_number}."
