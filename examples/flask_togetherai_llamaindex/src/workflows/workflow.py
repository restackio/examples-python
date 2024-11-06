from datetime import timedelta
from restack_ai.workflow import workflow, workflow_import, log

with workflow_import():
    from src.functions.llm_complete import llm_complete


@workflow.defn(name="llm_complete_workflow")
class llm_complete_workflow:
    @workflow.run
    async def run(self):
        log.info("Completing prompt")
        return await workflow.step(llm_complete, start_to_close_timeout=timedelta(seconds=120))
