from datetime import timedelta
from typing import Literal

from pydantic import BaseModel
from restack_ai.workflow import (
    NonRetryableError,
    ParentClosePolicy,
    log,
    workflow,
    workflow_info,
    import_functions
)

from src.agents.agent import AgentVideo

with import_functions():
    from src.functions.daily_create_room import DailyRoomInput, daily_create_room
    from src.functions.tavus_create_room import tavus_create_room

class RoomWorkflowOutput(BaseModel):
    room_url: str
    token: str | None = None


class RoomWorkflowInput(BaseModel):
    video_service: Literal["tavus", "heygen"]


class PipelineWorkflowInput(BaseModel):
    video_service: Literal["tavus", "heygen"]
    agent_name: str
    agent_id: str
    agent_run_id: str
    daily_room_url: str | None = None
    daily_room_token: str | None = None


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

            daily_room = None
            room_url = None
            
            if workflow_input.video_service == "heygen":
                daily_room = await workflow.step(
                    function=daily_create_room,
                    function_input=DailyRoomInput(
                        room_name=agent.run_id,
                    ),
                )
                room_url = daily_room.room_url

            if workflow_input.video_service == "tavus":
                tavus_room = await workflow.step(
                    function=tavus_create_room,
                )
                room_url = tavus_room.room_url

            await workflow.child_start(
                task_queue="pipeline",
                workflow="PipelineWorkflow",
                workflow_id=workflow_id,
                workflow_input=PipelineWorkflowInput(
                    video_service=workflow_input.video_service,
                    agent_name=AgentVideo.__name__,
                    agent_id=agent.id,
                    agent_run_id=agent.run_id,
                    daily_room_url=room_url if room_url else None,
                    daily_room_token=daily_room.token if daily_room else None,
                ),
                start_to_close_timeout=timedelta(minutes=20),
                parent_close_policy=ParentClosePolicy.ABANDON,
            )

        except Exception as e:
            error_message = f"Error during PipelineWorkflow: {e}"
            raise NonRetryableError(error_message) from e

        else:
            log.info(
                "RoomWorkflow completed", room_url=room_url
            )

            return RoomWorkflowOutput(room_url=room_url, token=daily_room.token if daily_room else None)
