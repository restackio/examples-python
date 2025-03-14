from datetime import timedelta
from typing import Literal

from pydantic import BaseModel
from restack_ai.workflow import (
    NonRetryableError,
    import_functions,
    log,
    workflow,
)

with import_functions():
    from src.functions.pipeline_heygen import (
        PipecatPipelineHeygenInput,
        pipecat_pipeline_heygen,
    )
    from src.functions.pipeline_tavus import (
        PipecatPipelineTavusInput,
        pipecat_pipeline_tavus,
    )


class PipelineWorkflowOutput(BaseModel):
    room_url: str


class PipelineWorkflowInput(BaseModel):
    video_service: Literal["tavus", "heygen"]
    agent_name: str
    agent_id: str
    agent_run_id: str


@workflow.defn()
class PipelineWorkflow:
    @workflow.run
    async def run(
        self, workflow_input: PipelineWorkflowInput
    ) -> PipelineWorkflowOutput:
        try:
            if workflow_input.video_service == "tavus":
                room_url = await workflow.step(
                    task_queue="pipeline",
                    function=pipecat_pipeline_tavus,
                    function_input=PipecatPipelineTavusInput(
                        agent_name=workflow_input.agent_name,
                        agent_id=workflow_input.agent_id,
                        agent_run_id=workflow_input.agent_run_id,
                    ),
                    start_to_close_timeout=timedelta(minutes=20),
                )

            elif workflow_input.video_service == "heygen":
                room_url = await workflow.step(
                    task_queue="pipeline",
                    function=pipecat_pipeline_heygen,
                    function_input=PipecatPipelineHeygenInput(
                        agent_name=workflow_input.agent_name,
                        agent_id=workflow_input.agent_id,
                        agent_run_id=workflow_input.agent_run_id,
                    ),
                    start_to_close_timeout=timedelta(minutes=20),
                )

        except Exception as e:
            error_message = f"Error during pipecat_pipeline: {e}"
            raise NonRetryableError(error_message) from e
        else:
            log.info("Pipecat pipeline started")

            log.info(
                "PipelineWorkflow completed", room_url=room_url
            )

            return PipelineWorkflowOutput(room_url=room_url)
