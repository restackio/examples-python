from restack_ai.function import function, log
from restack_ai.agent import uuid
from pydantic import BaseModel

class TodoCreateParams(BaseModel):
    title: str

class TodoCreateResponse(BaseModel):
    id: str
    title: str

@function.defn()
async def todo_create(params: TodoCreateParams) -> TodoCreateResponse:
    try:
        todo_id = str(uuid.uuid4())
        todo_title = params.title
        return TodoCreateResponse(
            id=todo_id,
            title=todo_title
        )
    except Exception as e:
        log.error("todo_create function failed", error=e)
        raise e
