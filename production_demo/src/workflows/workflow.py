import asyncio
from datetime import timedelta
from pydantic import BaseModel, Field
from restack_ai.workflow import workflow, log, workflow_info, import_functions, NonRetryableError
from .child import ChildWorkflow, ChildWorkflowInput

with import_functions():
    from src.functions.generate import llm_generate, GenerateInput

class ExampleWorkflowInput(BaseModel):
    amount: int = Field(default=50)

@workflow.defn()
class ExampleWorkflow:
    @workflow.run
    async def run(self, input: ExampleWorkflowInput):
        
        try:
            # use the parent run id to create child workflow ids
            parent_workflow_id = workflow_info().workflow_id

            tasks = []
            for i in range(input.amount):
                log.info(f"Queue ChildWorkflow {i+1} for execution")
                task = workflow.child_execute(
                    workflow=ChildWorkflow, 
                    workflow_id=f"{parent_workflow_id}-child-execute-{i+1}",
                    workflow_input=ChildWorkflowInput(prompt="Generate a random joke in max 20 words."),
                )
                tasks.append(task)

            # Run all child workflows in parallel and wait for their results
            results = await asyncio.gather(*tasks)

            for i, result in enumerate(results, start=1):
                log.info(f"ChildWorkflow {i} completed", result=result)

            generated_text = await workflow.step(
                function=llm_generate,
                function_input=GenerateInput(prompt=f"Give me the top 3 unique jokes according to the results. {results}"),
                task_queue="llm",
                start_to_close_timeout=timedelta(minutes=2)
            )

            return {
                "top_jokes": generated_text,
                "results": results
            }

        except Exception as e:
            log.error(f"ExampleWorkflow failed {e}")
            raise NonRetryableError(message=f"ExampleWorkflow failed {e}") from e