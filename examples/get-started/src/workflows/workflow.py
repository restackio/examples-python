from datetime import timedelta
from restack_ai.workflow import workflow, import_functions

with import_functions():
    from src.functions.function import welcome, goodbye, InputParams


@workflow.defn(name="GreetingWorkflow")
class GreetingWorkflow:
    @workflow.run
    async def run(self):
        return await workflow.step(welcome, InputParams("world"), start_to_close_timeout=timedelta(seconds=120))
    async def goodbye(self):
        return await workflow.step(goodbye, InputParams("world"), start_to_close_timeout=timedelta(seconds=120))


