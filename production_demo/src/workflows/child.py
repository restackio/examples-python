from datetime import timedelta
from restack_ai.workflow import workflow, import_functions, log
with import_functions():
    from src.functions.function import example_function
    from src.functions.openai import openai_joke

@workflow.defn()
class ChildWorkflow:
    @workflow.run
    async def run(self):
        log.info("ChildWorkflow started")
        result = await workflow.step(example_function, input="first", start_to_close_timeout=timedelta(seconds=120))

        await workflow.sleep(1)

        result = await workflow.step(openai_joke, task_queue="openai", start_to_close_timeout=timedelta(seconds=120))

        log.info("ChildWorkflow completed", result=result)
        return result


