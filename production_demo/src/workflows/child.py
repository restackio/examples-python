from datetime import timedelta

from pydantic import BaseModel, Field
from restack_ai.workflow import import_functions, log, workflow

with import_functions():
    from src.functions.evaluate import EvaluateInput, llm_evaluate
    from src.functions.function import ExampleFunctionInput, example_function
    from src.functions.generate import GenerateInput, llm_generate


class ChildWorkflowInput(BaseModel):
    prompt: str = Field(default="Generate a random joke in max 20 words.")


@workflow.defn()
class ChildWorkflow:
    @workflow.run
    async def run(self, input: ChildWorkflowInput):
        log.info("ChildWorkflow started")
        await workflow.step(
            example_function,
            input=ExampleFunctionInput(name="John Doe"),
            start_to_close_timeout=timedelta(minutes=2),
        )

        await workflow.sleep(1)

        generated_text = await workflow.step(
            llm_generate,
            GenerateInput(prompt=input.prompt),
            task_queue="llm",
            start_to_close_timeout=timedelta(minutes=2),
        )

        evaluation = await workflow.step(
            llm_evaluate,
            EvaluateInput(generated_text=generated_text),
            task_queue="llm",
            start_to_close_timeout=timedelta(minutes=5),
        )

        return {
            "generated_text": generated_text,
            "evaluation": evaluation,
        }
