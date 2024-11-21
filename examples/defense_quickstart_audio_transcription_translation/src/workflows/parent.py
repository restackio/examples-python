from restack_ai.workflow import workflow, log, workflow_info
from dataclasses import dataclass
from .child import ChildWorkflow

@dataclass
class WorkflowInputParams:
    file_data: list[tuple[str, str]]

@workflow.defn()
class ParentWorkflow:
    @workflow.run
    async def run(self, input: WorkflowInputParams):
        parent_workflow_id = workflow_info().workflow_id

        log.info("ParentWorkflow started", input=input)

        child_workflow_results = []
        for file_data in input.file_data:
            result = await workflow.child_execute(ChildWorkflow, workflow_id=f"{parent_workflow_id}-child-execute-{file_data[0]}", input=WorkflowInputParams(file_data=file_data))
            child_workflow_results.append(result)

        log.info("ParentWorkflow completed", results=child_workflow_results)

        return child_workflow_results


