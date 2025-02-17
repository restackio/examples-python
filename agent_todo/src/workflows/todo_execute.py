from datetime import timedelta

from pydantic import BaseModel
from restack_ai.workflow import import_functions, log, workflow

with import_functions():
    from src.functions.get_random import RandomParams, get_random
    from src.functions.get_result import ResultParams, get_result


class TodoExecuteParams(BaseModel):
    todo_title: str
    todo_id: str


class TodoExecuteResponse(BaseModel):
    todo_id: str
    todo_title: str
    details: str
    status: str


@workflow.defn()
class TodoExecute:
    @workflow.run
    async def run(self, params: TodoExecuteParams) -> TodoExecuteResponse:
        log.info("TodoExecuteWorkflow started")
        random = await workflow.step(
            get_random,
            input=RandomParams(todo_title=params.todo_title),
            start_to_close_timeout=timedelta(seconds=120),
        )

        await workflow.sleep(2)

        result = await workflow.step(
            get_result,
            input=ResultParams(todo_title=params.todo_title, todo_id=params.todo_id),
            start_to_close_timeout=timedelta(seconds=120),
        )

        todo_details = TodoExecuteResponse(
            todo_id=params.todo_id,
            todo_title=params.todo_title,
            details=random,
            status=result.status,
        )
        log.info("TodoExecuteWorkflow done", result=todo_details)
        return todo_details
