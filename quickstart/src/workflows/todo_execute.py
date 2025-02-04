from datetime import timedelta
from pydantic import BaseModel
from restack_ai.workflow import workflow, import_functions, log

with import_functions():
    from src.functions.random import get_random, RandomParams
    from src.functions.result import get_result, ResultParams


class TodoExecuteParams(BaseModel):
    todoTitle: str
    todoId: str


class TodoExecuteResponse(BaseModel):
    todoId: str
    todoTitle: str
    details: str
    status: str


@workflow.defn()
class TodoExecute:
    @workflow.run
    async def run(self, params: TodoExecuteParams):
        log.info("TodoExecuteWorkflow started")
        random = await workflow.step(
            get_random,
            input=RandomParams(todoTile=params.todoTile),
            start_to_close_timeout=timedelta(seconds=120),
        )

        await workflow.sleep(timedelta(seconds=2))

        result = await workflow.step(
            get_result,
            input=ResultParams(todoTile=params.todoTile, todoId=params.todoId),
            start_to_close_timeout=timedelta(seconds=120),
        )

        todo_details = TodoExecuteResponse(
            todoId=params.todoId,
            todoTitle=params.todoTitle,
            details=random,
            status=result.status,
        )
        log.info("TodoExecuteWorkflow done", result=todo_details)
        return todo_details
