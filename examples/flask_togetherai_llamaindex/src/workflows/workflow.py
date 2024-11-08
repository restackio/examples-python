from datetime import timedelta
from restack_ai.workflow import workflow, import_functions
from restack_ai import log

with import_functions():
    from src.functions.llm_complete import llm_complete

@workflow.defn(name="llm_complete_workflow")
class llm_complete_workflow:
    @workflow.run
    async def run(self, input: str):
        result = await workflow.step(llm_complete, input, start_to_close_timeout=timedelta(seconds=120))
        log.info("Workflow result", result=result)
        return result
