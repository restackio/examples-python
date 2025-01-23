from datetime import timedelta
from restack_ai.workflow import workflow, import_functions, log

with import_functions():
    from src.functions.function import llm_complete, FunctionInputParams

@workflow.defn()
class LlmCompleteWorkflow:
    @workflow.run
    async def run(self, input: dict):
        log.info("LlmCompleteWorkflow started", input=input)
        prompt = input["prompt"]
        result = await workflow.step(llm_complete, FunctionInputParams(prompt=prompt), start_to_close_timeout=timedelta(seconds=120))
        log.info("LlmCompleteWorkflow completed", result=result)
        return result
