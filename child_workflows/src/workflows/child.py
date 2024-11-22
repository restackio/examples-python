from datetime import timedelta
from restack_ai.workflow import workflow, import_functions, log
with import_functions():
    from src.functions.function import welcome

@workflow.defn()
class ChildWorkflow:
    @workflow.run
    async def run(self):
        log.info("ChildWorkflow started")
        result = await workflow.step(welcome, input="world", start_to_close_timeout=timedelta(seconds=120))
        log.info("ChildWorkflow completed", result=result)
        return result


