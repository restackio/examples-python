from datetime import timedelta

from restack_ai.workflow import workflow, import_functions, log

with import_functions():
    from src.functions.function import example_function
    from src.functions.generate import llm_generate
    from src.functions.evaluate import llm_evaluate

@workflow.defn()
class ChildWorkflow:
    @workflow.run
    async def run(self):
        log.info("ChildWorkflow started")
        await workflow.step(example_function, input="first", start_to_close_timeout=timedelta(seconds=120))

        await workflow.sleep(1)

        generated_text = await workflow.step(
            llm_generate,
            "Generate a random joke in max 20 words.",
            task_queue="llm",
            start_to_close_timeout=timedelta(seconds=120)
        )

        evaluation = await workflow.step(
            llm_evaluate,
            generated_text,
            task_queue="llm",
            start_to_close_timeout=timedelta(seconds=120)
        )

        return {
            "generated_text": generated_text,
            "evaluation": evaluation
        }


