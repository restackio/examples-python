from datetime import timedelta
from pydantic import BaseModel, Field
from restack_ai.workflow import workflow, import_functions, log
with import_functions():
    from src.functions.function import welcome, WelcomeInput

class GreetingWorkflowInput(BaseModel):
    name: str = Field(default='Bob')

@workflow.defn()
class GreetingWorkflow:
    @workflow.run
    async def run(self, input: GreetingWorkflowInput):
        log.info("GreetingWorkflow started")
        result = await workflow.step(welcome, input=WelcomeInput(name=input.name), start_to_close_timeout=timedelta(seconds=120))
        log.info("GreetingWorkflow completed", result=result)
        return result


