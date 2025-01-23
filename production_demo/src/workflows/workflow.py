import asyncio
from datetime import timedelta
from pydantic import BaseModel, Field
from restack_ai.workflow import workflow, log, workflow_info, import_functions
from .child import ChildWorkflow, ChildWorkflowInput

with import_functions():
    from src.functions.generate import llm_generate, GenerateInput

class ExampleWorkflowInput(BaseModel):
    amount: int = Field(default=50)

@workflow.defn()
class ExampleWorkflow:
    @workflow.run
    async def run(self, input: ExampleWorkflowInput):
        # use the parent run id to create child workflow ids
        parent_workflow_id = workflow_info().workflow_id

        tasks = []
        for i in range(input.amount):
            log.info(f"Queue ChildWorkflow {i+1} for execution")
            task = workflow.child_execute(
                ChildWorkflow, 
                workflow_id=f"{parent_workflow_id}-child-execute-{i+1}",
                input=ChildWorkflowInput(name=f"child workflow {i+1}")
            )
            tasks.append(task)

        # Run all child workflows in parallel and wait for their results
        results = await asyncio.gather(*tasks)

        for i, result in enumerate(results, start=1):
            log.info(f"ChildWorkflow {i} completed", result=result)

        generated_text = await workflow.step(
            llm_generate,
            GenerateInput(prompt=f"Give me the top 3 unique jokes according to the results. {results}"),
            task_queue="llm",
            start_to_close_timeout=timedelta(minutes=2)
        )

        return {
            "top_jokes": generated_text,
            "results": results
        }

