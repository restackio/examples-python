import asyncio
from datetime import timedelta

from restack_ai.workflow import workflow, log, workflow_info, import_functions
from .child import ChildWorkflow

with import_functions():
    from src.functions.generate import llm_generate

@workflow.defn()
class ExampleWorkflow:
    @workflow.run
    async def run(self):
        # use the parent run id to create child workflow ids
        parent_workflow_id = workflow_info().workflow_id

        tasks = []
        for i in range(100):
            log.info(f"Queue ChildWorkflow {i+1} for execution")
            task = workflow.child_execute(
                ChildWorkflow, 
                workflow_id=f"{parent_workflow_id}-child-execute-{i+1}"
            )
            tasks.append(task)

        # Run all child workflows in parallel and wait for their results
        results = await asyncio.gather(*tasks)

        for i, result in enumerate(results, start=1):
            log.info(f"ChildWorkflow {i} completed", result=result)

        generated_text = await workflow.step(
            llm_generate,
            f"Give me the top 3 jokes according to the results. {results}",
            task_queue="llm",
            start_to_close_timeout=timedelta(seconds=120)
        )

        return {
            "top_jokes": generated_text,
            "results": results
        }

