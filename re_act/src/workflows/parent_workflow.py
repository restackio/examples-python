from dataclasses import dataclass
from datetime import timedelta

from restack_ai.workflow import import_functions, workflow, workflow_info

from .child_workflow_a import ChildWorkflowA
from .child_workflow_b import ChildWorkflowB

with import_functions():
    from src.functions.decide import DecideInput, decide


@dataclass
class ParentWorkflowInput:
    email: str
    current_accepted_applicants_count: int


@workflow.defn()
class ParentWorkflow:
    @workflow.run
    async def run(self, parent_workflow_input: ParentWorkflowInput) -> None:
        parent_workflow_id = workflow_info().workflow_id

        decide_result = await workflow.step(
            decide,
            input=DecideInput(
                email=parent_workflow_input.email,
                current_accepted_applicants_count=parent_workflow_input.current_accepted_applicants_count,
            ),
            start_to_close_timeout=timedelta(seconds=120),
        )

        decision = decide_result[0]["function"]["name"]

        if decision == "accept_applicant":
            await workflow.child_execute(
                ChildWorkflowA,
                workflow_id=f"{parent_workflow_id}-child-a",
                input=parent_workflow_input.email,
            )
        elif decision == "reject_applicant":
            await workflow.child_execute(
                ChildWorkflowB,
                workflow_id=f"{parent_workflow_id}-child-b",
                input=parent_workflow_input.email,
            )
