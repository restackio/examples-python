import secrets

from pydantic import BaseModel
from restack_ai.function import NonRetryableError, function


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
        error_message = "Error during get_result function"
        raise NonRetryableError(message=error_message, error=e) from e
