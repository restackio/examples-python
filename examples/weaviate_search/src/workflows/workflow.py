from datetime import timedelta
from restack_ai.workflow import workflow, import_functions, log

with import_functions():
    from src.functions.seed_database import seed_database
    from src.functions.vector_search import vector_search

@workflow.defn()
class SeedWorkflow:
    @workflow.run
    async def run(self):
        seed_result = await workflow.step(seed_database, start_to_close_timeout=timedelta(seconds=120))
        log.info("SeedWorkflow completed", seed_result=seed_result)
        return seed_result

@workflow.defn()
class SearchWorkflow:
    @workflow.run
    async def run(self):
        search_result = await workflow.step(vector_search, start_to_close_timeout=timedelta(seconds=120))
        log.info("SearchWorkflow completed", search_result=search_result)
        return search_result
