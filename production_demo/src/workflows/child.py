from datetime import timedelta
from pydantic import BaseModel, Field
from restack_ai.workflow import workflow, import_functions, log, NonRetryableError, RetryPolicy

with import_functions():
    from src.functions.function import example_function, ExampleFunctionInput
    from src.functions.generate import llm_generate, GenerateInput
    from src.functions.evaluate import llm_evaluate, EvaluateInput

class ChildWorkflowInput(BaseModel):
    prompt: str = Field(default="Generate a random joke in max 20 words.")

@workflow.defn()
class ChildWorkflow:
    @workflow.run
    async def run(self, input: ChildWorkflowInput):
        
        log.info("ChildWorkflow started")

        try:
            await workflow.step(function=example_function, function_input=ExampleFunctionInput(name='John Doe'), start_to_close_timeout=timedelta(minutes=2), retry_policy=RetryPolicy(maximum_attempts=3))

            await workflow.sleep(1)

            generated_text = await workflow.step(
                function=llm_generate,
                function_input=GenerateInput(prompt=input.prompt),
                task_queue="llm",
                start_to_close_timeout=timedelta(minutes=2)
            )

            evaluation = await workflow.step(
                function=llm_evaluate,
                function_input=EvaluateInput(generated_text=generated_text),
                task_queue="llm",
                start_to_close_timeout=timedelta(minutes=5)
            )

            return {
                "generated_text": generated_text,
                "evaluation": evaluation
            }
        except Exception as e:
            log.error(f"ChildWorkflow failed {e}")
            raise NonRetryableError(message=f"ChildWorkflow failed {e}") from e


