from datetime import timedelta
from pydantic import BaseModel, Field
from restack_ai.workflow import workflow, import_functions, log, RetryPolicy
with import_functions():
    from src.functions.e2b_execute_python import e2b_execute_python, ExecutePythonInput
    from src.functions.openai_tool_call import openai_tool_call, OpenaiToolCallInput

class E2BWorkflowInput(BaseModel):
    name: str = Field(default=' ')

class E2BWorkflowOutput(BaseModel):
    stdout: list[str]
    stderr: list[str]

@workflow.defn()
class E2BWorkflow:
    @workflow.run
    async def run(self, input: E2BWorkflowInput):
        result = await workflow.step(e2b_execute_python, input={"code": "print('Hello World')"}, retry_policy=RetryPolicy(maximum_attempts=1))
        return E2BWorkflowOutput(stdout=result["stdout"], stderr=result["stderr"])
