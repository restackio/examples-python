import asyncio

from pydantic import BaseModel, Field
from restack_ai.workflow import NonRetryableError, log, workflow, workflow_info

from .pdf import PdfWorkflow, PdfWorkflowInput


class FilesWorkflowInput(BaseModel):
    files_upload: list[dict] = Field(files=True)

@workflow.defn()
class FilesWorkflow:
    @workflow.run
    async def run(self, input: FilesWorkflowInput):
        tasks = []
        parent_workflow_id = workflow_info().workflow_id

        for index, pdf_input in enumerate(input.files_upload, start=1):
            log.info(f"Queue PdfWorkflow {index} for execution")
            # Ensure child workflows are started and return an awaitable
            try:
                task = workflow.child_execute(
                    workflow=PdfWorkflow,
                    workflow_id=f"{parent_workflow_id}-pdf-{index}",
                    input=PdfWorkflowInput(
                        file_upload=[pdf_input]
                    )
                )
            except Exception as e:
                error_message = f"Failed to execute PdfWorkflow {index}: {e}"
                raise NonRetryableError(error_message) from e
            else:
                # Wrap the task in an asyncio.ensure_future to ensure it's awaitable
                tasks.append(asyncio.ensure_future(task))

        # Await all tasks at once to run them in parallel
        results = await asyncio.gather(*tasks)

        for i, result in enumerate(results, start=1):
            log.info(f"PdfWorkflow {i} completed", result=result)

        return {
            "results": results
        }
