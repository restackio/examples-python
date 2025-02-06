from datetime import timedelta

from pydantic import BaseModel, Field
from restack_ai.workflow import import_functions, log, workflow

with import_functions():
    from src.functions.function import WelcomeInput, welcome


class GreetingWorkflowInput(BaseModel):
    name: str = Field(default="Bob")


@workflow.defn()
class GreetingWorkflow:
    @workflow.run
    async def run(self, greeting_workflow_input: GreetingWorkflowInput) -> str:
        log.info("GreetingWorkflow started")
        result = await workflow.step(
            welcome,
            input=WelcomeInput(name=greeting_workflow_input.name),
            start_to_close_timeout=timedelta(seconds=120),
        )
        log.info("GreetingWorkflow completed", result=result)
        return result
