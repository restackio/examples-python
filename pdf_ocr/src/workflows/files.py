from restack_ai.workflow import workflow, log, workflow_info
from typing import List
from pydantic import BaseModel, Field
import asyncio
from .pdf import PdfWorkflow, PdfWorkflowInput


class FilesWorkflowInput(BaseModel):
    files_upload: List[dict] = Field(files=True)

@workflow.defn()
class FilesWorkflow:
    @workflow.run
    async def run(self, input: FilesWorkflowInput):
        tasks = []
        parent_workflow_id = workflow_info().workflow_id

        for index, pdf_input in enumerate(input.files_upload, start=1):
            log.info(f"Queue PdfWorkflow {index} for execution")
            # Ensure child workflows are started and return an awaitable
            task = workflow.child_execute(
                PdfWorkflow, 
                workflow_id=f"{parent_workflow_id}-pdf-{index}",
                input=PdfWorkflowInput(
                    file_upload=[pdf_input]
                )
            )
            # Wrap the task in an asyncio.ensure_future to ensure it's awaitable
            tasks.append(asyncio.ensure_future(task))

        # Await all tasks at once to run them in parallel
        results = await asyncio.gather(*tasks)

        for i, result in enumerate(results, start=1):
            log.info(f"PdfWorkflow {i} completed", result=result)

        return {
            "results": results
        }
