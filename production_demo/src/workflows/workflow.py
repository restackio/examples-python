from restack_ai.workflow import workflow, log, workflow_info
import asyncio

from .child import ChildWorkflow

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

        return results

