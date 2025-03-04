import secrets

from pydantic import BaseModel
from restack_ai.function import NonRetryableError, function, log


class TodoCreateParams(BaseModel):
    title: str


@function.defn()
async def todo_create(params: TodoCreateParams) -> str:
    try:
        log.info("todo_create function start", title=params.title)

        todo_id = f"todo-{secrets.randbelow(9000) + 1000}"
    except Exception as e:
        error_message = f"todo_create function failed: {e}"
        raise NonRetryableError(error_message) from e
    else:
        log.info("todo_create function completed", todo_id=todo_id)
        return f"Created the todo '{params.title}' with id: {todo_id}"
