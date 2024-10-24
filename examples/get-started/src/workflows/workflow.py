from datetime import timedelta
from restack_ai.workflow import workflow
from temporalio import workflow as temporal_workflow

with temporal_workflow.unsafe.imports_passed_through():
    from src.functions.function import welcome, InputParams
with temporal_workflow.unsafe.imports_passed_through():
    from src.functions.query import query

@workflow.defn(name="GreetingWorkflow")
class GreetingWorkflow:
    @workflow.run
    async def run(self):
        return await workflow.step(welcome, InputParams("world"), start_to_close_timeout=timedelta(seconds=10))

@workflow.defn(name="QueryWorkflow")
class QueryWorkflow:
    @workflow.run
    async def run(self):
        return await workflow.step(query, start_to_close_timeout=timedelta(seconds=10))



