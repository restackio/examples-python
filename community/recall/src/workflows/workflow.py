import asyncio
from datetime import timedelta
from pydantic import BaseModel, Field
from restack_ai.workflow import workflow, log, workflow_info, import_functions
from .summarize_meeting import SummarizeMeetingWorkflow, SummarizeMeetingInput

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
            log.info(f"Queue SummarizeMeetingWorkflow {i+1} for execution")
            task = workflow.child_execute(
                SummarizeMeetingWorkflow, 
                workflow_id=f"{parent_workflow_id}-child-execute-{i+1}",
                input=SummarizeMeetingInput(meeting_url=f"https://meet.google.com/abc-def-ghi")
            )
            tasks.append(task)

        # Run all child workflows in parallel and wait for their results
        results = await asyncio.gather(*tasks)

        for i, result in enumerate(results, start=1):
            log.info(f"SummarizeMeetingWorkflow {i} completed", result=result)
        
        return {
            "results": results
        }

