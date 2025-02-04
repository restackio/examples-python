from restack_ai.workflow import workflow, log, workflow_info
from pydantic import BaseModel
from .child import ChildWorkflow, ChildInput

class ParentInput(BaseModel):
    child: bool = True

class ParentOutput(BaseModel):
    result: str

@workflow.defn()
class ParentWorkflow:
    @workflow.run
    async def run(self, input: ParentInput) -> ParentOutput:
        if input.child:
            # use the parent run id to create child workflow ids
            parent_workflow_id = workflow_info().workflow_id

            log.info("Start ChildWorkflow and dont wait for result")
            result = await workflow.child_start(ChildWorkflow, input=ChildInput(name="world"), workflow_id=f"{parent_workflow_id}-child-start")
            
            log.info("Start ChildWorkflow and wait for result")
            result = await workflow.child_execute(ChildWorkflow, input=ChildInput(name="world"), workflow_id=f"{parent_workflow_id}-child-execute")
            log.info("ChildWorkflow completed", result=result)
            return ParentOutput(result="ParentWorkflow completed")
        
        else:
            log.info("ParentWorkflow without starting or executing child workflow")
            return ParentOutput(result="ParentWorkflow completed")
