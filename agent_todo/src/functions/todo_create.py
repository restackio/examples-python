import secrets

from pydantic import BaseModel
from restack_ai.function import function, log


class TodoCreateParams(BaseModel):
    title: str


@function.defn()
async def todo_create(params: TodoCreateParams) -> str:
    try:
        log.info("todo_create function start", title=params.title)

        todo_id = f"todo-{secrets.randbelow(9000) + 1000}"
    except Exception as e:
        log.error("todo_create function failed", error=e)
        raise
    else:
        log.info("todo_create function completed", todo_id=todo_id)
        return f"Created the todo '{params.title}' with id: {todo_id}"
