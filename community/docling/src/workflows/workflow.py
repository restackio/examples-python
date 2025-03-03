from datetime import timedelta
from pydantic import BaseModel
from restack_ai.workflow import workflow, import_functions, log
with import_functions():
    from src.functions.function import welcome
    

class Input(BaseModel):
    name: str = "world"

class Output(BaseModel):
    result: str

@workflow.defn()
class Workflow:
    @workflow.run
    async def run(self, workflow_input: Input) -> Output:
        log.info("ChildWorkflow started")
        result = await workflow.step(function=welcome, function_input=workflow_input.name, start_to_close_timeout=timedelta(seconds=120))
        log.info("ChildWorkflow completed", result=result)
        return Output(result=result)
