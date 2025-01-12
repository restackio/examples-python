from datetime import timedelta
from pydantic import BaseModel, Field
from restack_ai.workflow import workflow, import_functions, log

with import_functions():
    from src.functions.function import example_function
    from src.functions.generate import llm_generate, GenerateInput
    from src.functions.evaluate import llm_evaluate, EvaluateInput

class ChildWorkflowInput(BaseModel):
    name: str = Field(default='John Doe')

@workflow.defn()
class ChildWorkflow:
    @workflow.run
    async def run(self, input: ChildWorkflowInput):
        log.info("ChildWorkflow started")
        await workflow.step(example_function, input=input, start_to_close_timeout=timedelta(minutes=2))

        await workflow.sleep(1)

        generated_text = await workflow.step(
            llm_generate,
            GenerateInput(prompt="Generate a random joke in max 20 words."),
            task_queue="llm",
            start_to_close_timeout=timedelta(minutes=2)
        )

        evaluation = await workflow.step(
            llm_evaluate,
            EvaluateInput(generated_text=generated_text),
            task_queue="llm",
            start_to_close_timeout=timedelta(minutes=2)
        )

        return {
            "generated_text": generated_text,
            "evaluation": evaluation
        }


