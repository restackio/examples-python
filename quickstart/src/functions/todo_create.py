from restack_ai.function import function, log
import random
from pydantic import BaseModel

class TodoCreateParams(BaseModel):
    title: str

@function.defn()
async def todo_create(params: TodoCreateParams) -> str:
    try:
        
        log.info("todo_create function start", title=params.title)

        todo_id = f"todo-{random.randint(1000, 9999)}"

        log.info("todo_create function completed", todo_id=todo_id)
        return todo_id
    except Exception as e:
        log.error("todo_create function failed", error=e)
        raise e
