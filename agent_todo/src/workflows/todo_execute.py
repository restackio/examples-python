from datetime import timedelta

from pydantic import BaseModel
from restack_ai.workflow import (
    NonRetryableError,
    import_functions,
    log,
    workflow,
)

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
    async def run(self, workflow_input: TodoExecuteParams) -> TodoExecuteResponse:
        log.info("TodoExecuteWorkflow started")
        try:
            random = await workflow.step(
                function=get_random,
                function_input=RandomParams(todo_title=workflow_input.todo_title),
                start_to_close_timeout=timedelta(seconds=120),
            )
        except Exception as e:
            error_message = f"Error during get_random: {e}"
            raise NonRetryableError(error_message) from e
        else:
            log.info("get_random done", random=random)

            await workflow.sleep(2)

            try:
                result = await workflow.step(
                    function=get_result,
                    function_input=ResultParams(
                        todo_title=workflow_input.todo_title,
                        todo_id=workflow_input.todo_id,
                    ),
                    start_to_close_timeout=timedelta(seconds=120),
                )
            except Exception as e:
                error_message = f"Error during get_result: {e}"
                raise NonRetryableError(error_message) from e
            else:
                todo_details = TodoExecuteResponse(
                    todo_id=workflow_input.todo_id,
                    todo_title=workflow_input.todo_title,
                    details=random,
                    status=result.status,
                )
                log.info("TodoExecuteWorkflow done", result=todo_details)
                return todo_details
