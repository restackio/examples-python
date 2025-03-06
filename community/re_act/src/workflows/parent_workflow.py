from restack_ai.workflow import workflow, log, workflow_info, import_functions
from datetime import timedelta
import json
from dataclasses import dataclass
from .child_workflow_a import ChildWorkflowA
from .child_workflow_b import ChildWorkflowB

with import_functions():
    from src.functions.decide import decide, DecideInput

@dataclass
class ParentWorkflowInput:
    email: str
    current_accepted_applicants_count: int

@workflow.defn()
class ParentWorkflow:
    @workflow.run
    async def run(self, input: ParentWorkflowInput):
        parent_workflow_id = workflow_info().workflow_id

        decide_result = await workflow.step(
            decide,
            input=DecideInput(
                email=input.email,
                current_accepted_applicants_count=input.current_accepted_applicants_count
            ),
            start_to_close_timeout=timedelta(seconds=120)
        )

        decision = decide_result[0]['function']['name']

        child_workflow_result = None
        if decision == "accept_applicant":
            child_workflow_result = await workflow.child_execute(
                ChildWorkflowA,
                workflow_id=f"{parent_workflow_id}-child-a",
                input=input.email
            )
        elif decision == "reject_applicant":
            child_workflow_result = await workflow.child_execute(
                ChildWorkflowB,
                workflow_id=f"{parent_workflow_id}-child-b",
                input=input.email
            )

        return child_workflow_result


