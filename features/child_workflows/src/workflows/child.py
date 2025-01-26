from datetime import timedelta
from pydantic import BaseModel
from restack_ai.workflow import workflow, import_functions, log
with import_functions():
    from src.functions.function import welcome
    

class ChildInput(BaseModel):
    name: str = "world"

class ChildOutput(BaseModel):
    result: str

@workflow.defn()
class ChildWorkflow:
    @workflow.run
    async def run(self, input: ChildInput) -> ChildOutput:
        log.info("ChildWorkflow started")
        result = await workflow.step(welcome, input=input.name, start_to_close_timeout=timedelta(seconds=120))
        log.info("ChildWorkflow completed", result=result)
        return ChildOutput(result=result)
