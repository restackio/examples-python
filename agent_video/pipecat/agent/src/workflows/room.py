from datetime import timedelta
from typing import Literal

from pydantic import BaseModel
from restack_ai.workflow import (
    NonRetryableError,
    ParentClosePolicy,
    log,
    workflow,
    workflow_info,
)

from src.agents.agent import AgentVideo


class RoomWorkflowOutput(BaseModel):
    room_url: str


class RoomWorkflowInput(BaseModel):
    video_service: Literal["tavus", "heygen"]


class PipelineWorkflowInput(BaseModel):
    video_service: Literal["tavus", "heygen"]
    agent_name: str
    agent_id: str
    agent_run_id: str


@workflow.defn()
class RoomWorkflow:
    @workflow.run
    async def run(
        self, workflow_input: RoomWorkflowInput
    ) -> RoomWorkflowOutput:
        agent_id = f"{workflow_info().workflow_id}-agent"
        try:
            agent = await workflow.child_start(
                agent=AgentVideo,
                agent_id=agent_id,
                start_to_close_timeout=timedelta(minutes=20),
                parent_close_policy=ParentClosePolicy.ABANDON,
            )

            workflow_id = f"{agent.run_id}-pipeline"
            room: RoomWorkflowOutput = await workflow.child_execute(
                task_queue="pipeline",
                workflow="PipelineWorkflow",
                workflow_id=workflow_id,
                workflow_input=PipelineWorkflowInput(
                    video_service=workflow_input.video_service,
                    agent_name=AgentVideo.__name__,
                    agent_id=agent.id,
                    agent_run_id=agent.run_id,
                ),
                start_to_close_timeout=timedelta(minutes=20),
                parent_close_policy=ParentClosePolicy.ABANDON,
            )

            room_url = room.get("room_url")

        except Exception as e:
            error_message = f"Error during PipelineWorkflow: {e}"
            raise NonRetryableError(error_message) from e

        else:
            log.info(
                "RoomWorkflow completed", room_url=room_url
            )

            return RoomWorkflowOutput(room_url=room_url)
