from datetime import timedelta

from restack_ai.workflow import import_functions, log, workflow

with import_functions():
    from src.functions.function import FunctionInputParams, llm_complete


@workflow.defn()
class LlmCompleteWorkflow:
    @workflow.run
    async def run(self, llm_complete_input: dict) -> str:
        log.info("LlmCompleteWorkflow started", input=llm_complete_input)
        prompt = llm_complete_input["prompt"]
        result = await workflow.step(
            llm_complete,
            FunctionInputParams(prompt=prompt),
            start_to_close_timeout=timedelta(seconds=120),
        )
        log.info("LlmCompleteWorkflow completed", result=result)
        return result
