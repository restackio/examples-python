from restack_ai.workflow import workflow, log, workflow_info

from .child import ChildWorkflow

@workflow.defn()
class ParentWorkflow:
    @workflow.run
    async def run(self):
        

        # use the parent run id to create child workflow ids

        parent_workflow_id = workflow_info().workflow_id

        log.info("Start ChildWorkflow and dont wait for result")

        result = await workflow.child_start(ChildWorkflow, workflow_id=f"{parent_workflow_id}-child-start")

        log.info("Start ChildWorkflow and wait for result")
        result = await workflow.child_execute(ChildWorkflow, workflow_id=f"{parent_workflow_id}-child-execute")
        log.info("ChildWorkflow completed", result=result)
        return result


