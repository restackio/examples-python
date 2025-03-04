from pydantic import BaseModel
from restack_ai.workflow import NonRetryableError, log, workflow, workflow_info

from .child import ChildInput, ChildWorkflow


class ParentInput(BaseModel):
    child: bool = True

class ParentOutput(BaseModel):
    result: str

@workflow.defn()
class ParentWorkflow:
    @workflow.run
    async def run(self, workflow_input: ParentInput) -> ParentOutput:

        log.info("ParentWorkflow started", workflow_input=workflow_input)
        if workflow_input.child:
            # use the parent run id to create child workflow ids
            parent_workflow_id = workflow_info().workflow_id

            log.info("Start ChildWorkflow and dont wait for result")
            # result = await workflow.child_start(ChildWorkflow, input=ChildInput(name="world"), workflow_id=f"{parent_workflow_id}-child-start")

            log.info("Start ChildWorkflow and wait for result")
            try:
                result = await workflow.child_execute(
                    workflow=ChildWorkflow,
                    workflow_input=ChildInput(name="world"),
                    workflow_id=f"{parent_workflow_id}-child-execute",
                )
            except Exception as e:
                error_message = f"Error during child_execute: {e}"
                raise NonRetryableError(error_message) from e
            else:
                log.info("ChildWorkflow completed", result=result)
                return ParentOutput(result="ParentWorkflow completed")

        else:
            log.info("ParentWorkflow without starting or executing child workflow")
            return ParentOutput(result="ParentWorkflow completed")
