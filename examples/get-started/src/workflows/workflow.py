from datetime import timedelta
from restack_ai.workflow import workflow, import_functions, log
with import_functions():
    from src.functions.function import welcome

@workflow.defn(name="GreetingWorkflow")
class GreetingWorkflow:
    @workflow.run
    async def run(self):
        log.info("GreetingWorkflow started")
        result = await workflow.step(welcome, input="world", start_to_close_timeout=timedelta(seconds=120))
        log.info("GreetingWorkflow completed", result=result)
        return result


