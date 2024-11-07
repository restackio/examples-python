from datetime import timedelta
from restack_ai.workflow import workflow, workflow_import

with workflow_import():
    from src.functions.function import llm_complete, FunctionInputParams

@workflow.defn(name="llm_complete_workflow")
class llm_complete_workflow:
    @workflow.run
    async def run(self, input: dict):
        prompt = input["prompt"]
        return await workflow.step(llm_complete, FunctionInputParams(prompt=prompt), start_to_close_timeout=timedelta(seconds=120))
