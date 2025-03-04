from datetime import timedelta

from pydantic import BaseModel
from restack_ai.workflow import NonRetryableError, import_functions, log, workflow

with import_functions():
    from src.functions.function import welcome


class ChildInput(BaseModel):
    name: str = "world"

class ChildOutput(BaseModel):
    result: str

@workflow.defn()
class ChildWorkflow:
    @workflow.run
    async def run(self, workflow_input: ChildInput) -> ChildOutput:
        log.info("ChildWorkflow started")
        try:
            result = await workflow.step(
                function=welcome,
                function_input=workflow_input.name,
                start_to_close_timeout=timedelta(seconds=120)
            )
        except Exception as e:
            error_message = f"Error during welcome: {e}"
            raise NonRetryableError(error_message) from e
        else:
            log.info("ChildWorkflow completed", result=result)
            return ChildOutput(result=result)
