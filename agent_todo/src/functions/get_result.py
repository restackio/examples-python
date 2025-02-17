import secrets

from pydantic import BaseModel
from restack_ai.function import function, log


class ResultParams(BaseModel):
    todo_title: str
    todo_id: str


class ResultResponse(BaseModel):
    status: str
    todo_id: str


@function.defn()
async def get_result(params: ResultParams) -> ResultResponse:
    try:
        status = secrets.choice(["completed", "failed"])
        return ResultResponse(todo_id=params.todo_id, status=status)
    except Exception as e:
        log.error("result function failed", error=e)
        raise
