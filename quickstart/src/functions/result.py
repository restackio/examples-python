from restack_ai.function import function, log
from pydantic import BaseModel
import random


class ResultParams(BaseModel):
    todoTile: str
    todoId: str


class ResultResponse(BaseModel):
    status: str
    todoId: str


@function.defn()
async def get_result(params: ResultParams) -> ResultResponse:
    try:
        status = random.choice(["completed", "failed"])
        return ResultResponse(todoId=params.todoId, status=status)
    except Exception as e:
        log.error("result function failed", error=e)
        raise e
