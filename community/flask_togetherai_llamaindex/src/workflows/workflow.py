from datetime import timedelta

from restack_ai.workflow import import_functions, log, workflow

with import_functions():
    from src.functions.llm_complete import llm_complete


@workflow.defn()
class LlmCompleteWorkflow:
    @workflow.run
    async def run(self, llm_complete_input: str) -> str:
        log.info("LlmCompleteWorkflow started", input=llm_complete_input)
        result = await workflow.step(
            llm_complete,
            llm_complete_input,
            start_to_close_timeout=timedelta(seconds=120),
        )
        log.info("LlmCompleteWorkflow completed", result=result)
        return result
