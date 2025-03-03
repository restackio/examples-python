from datetime import timedelta

from pydantic import BaseModel
from restack_ai.workflow import (
    ParentClosePolicy,
    import_functions,
    log,
    workflow,
    workflow_info,
)

from src.agents.agent import AgentVideo

with import_functions():
    from src.functions.pipeline import PipecatPipelineInput, pipecat_pipeline


class RoomWorkflowOutput(BaseModel):
    room_url: str


@workflow.defn()
class RoomWorkflow:
    @workflow.run
    async def run(self) -> RoomWorkflowOutput:
        agent_id = f"{workflow_info().workflow_id}-agent"
        agent = await workflow.child_start(
            agent=AgentVideo,
            agent_id=agent_id,
            start_to_close_timeout=timedelta(minutes=20),
            parent_close_policy=ParentClosePolicy.ABANDON,
        )

        log.info("Agent started", agent=agent)

        room_url = await workflow.step(
            function=pipecat_pipeline,
            function_input=PipecatPipelineInput(
                agent_name=AgentVideo.__name__,
                agent_id=agent.id,
                agent_run_id=agent.run_id,
            ),
            start_to_close_timeout=timedelta(minutes=20),
        )

        log.info("Pipecat pipeline started")

        log.info("RoomWorkflow completed", room_url=room_url)

        return RoomWorkflowOutput(room_url=room_url)
