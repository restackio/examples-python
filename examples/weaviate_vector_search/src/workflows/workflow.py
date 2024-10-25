from datetime import timedelta
from restack_ai.workflow import workflow
from temporalio import workflow as temporal_workflow

with temporal_workflow.unsafe.imports_passed_through():
    from src.functions.seed_database import seed_database
with temporal_workflow.unsafe.imports_passed_through():
    from src.functions.vector_search import vector_search

@workflow.defn(name="seed_workflow")
class seed_workflow:
    @workflow.run
    async def run(self):
        return await workflow.step(seed_database, start_to_close_timeout=timedelta(seconds=10))

@workflow.defn(name="search_workflow")
class search_workflow:
    @workflow.run
    async def run(self):
        return await workflow.step(vector_search, start_to_close_timeout=timedelta(seconds=10))
