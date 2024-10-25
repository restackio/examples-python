from datetime import timedelta
from restack_ai.workflow import workflow, workflow_import 

with workflow_import():
    from src.functions.function import welcome, goodbye, InputParams

@workflow.defn(name="GreetingWorkflow")
class GreetingWorkflow:
    @workflow.run
    async def run(self):
        welcome_result = await workflow.step(welcome, InputParams("world"), start_to_close_timeout=timedelta(seconds=10))
        goodbye_result = await workflow.step(goodbye, InputParams("world"), start_to_close_timeout=timedelta(seconds=10))
        return f"{welcome_result} {goodbye_result}"


