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
    from src.functions.daily_delete_room import (
        DailyDeleteRoomInput,
        daily_delete_room,
    )
    from src.functions.pipeline_audio import (
        PipecatPipelineAudioInput,
        pipecat_pipeline_audio,
    )
    from src.functions.pipeline_heygen import (
        PipecatPipelineHeygenInput,
        pipecat_pipeline_heygen,
    )
    from src.functions.pipeline_tavus import (
        PipecatPipelineTavusInput,
        pipecat_pipeline_tavus,
    )
    from src.functions.send_agent_event import (
        SendAgentEventInput,
        send_agent_event,
    )


class PipelineWorkflowInput(BaseModel):
    video_service: Literal["tavus", "heygen", "audio"]
    agent_name: str
    agent_id: str
    agent_run_id: str
    daily_room_url: str | None = None
    daily_room_token: str | None = None


@workflow.defn()
class PipelineWorkflow:
    @workflow.run
    async def run(
        self, workflow_input: PipelineWorkflowInput
    ) -> bool:
        try:
            if workflow_input.video_service == "tavus":
                await workflow.step(
                    task_queue="pipeline",
                    function=pipecat_pipeline_tavus,
                    function_input=PipecatPipelineTavusInput(
                        agent_name=workflow_input.agent_name,
                        agent_id=workflow_input.agent_id,
                        agent_run_id=workflow_input.agent_run_id,
                        daily_room_url=workflow_input.daily_room_url,
                    ),
                    start_to_close_timeout=timedelta(minutes=20),
                )

            elif workflow_input.video_service == "heygen":
                try:
                    await workflow.step(
                        task_queue="pipeline",
                        function=pipecat_pipeline_heygen,
                        function_input=PipecatPipelineHeygenInput(
                            agent_name=workflow_input.agent_name,
                            agent_id=workflow_input.agent_id,
                            agent_run_id=workflow_input.agent_run_id,
                            daily_room_url=workflow_input.daily_room_url,
                            daily_room_token=workflow_input.daily_room_token,
                        ),
                        start_to_close_timeout=timedelta(
                            minutes=20
                        ),
                    )

                except Exception as e:
                    log.error("Error heygen pipeline", error=e)
                    await workflow.step(
                        task_queue="pipeline",
                        function=daily_delete_room,
                        function_input=DailyDeleteRoomInput(
                            room_name=workflow_input.agent_run_id,
                        ),
                    )

                await workflow.step(
                    task_queue="pipeline",
                    function=daily_delete_room,
                    function_input=DailyDeleteRoomInput(
                        room_name=workflow_input.agent_run_id,
                    ),
                )

                await workflow.step(
                    task_queue="pipeline",
                    function=send_agent_event,
                    function_input=SendAgentEventInput(
                        event_name="end",
                        agent_id=workflow_input.agent_id,
                        run_id=workflow_input.agent_run_id,
                    ),
                )

            elif workflow_input.video_service == "audio":
                try:
                    await workflow.step(
                        task_queue="pipeline",
                        function=pipecat_pipeline_audio,
                        function_input=PipecatPipelineAudioInput(
                            agent_name=workflow_input.agent_name,
                            agent_id=workflow_input.agent_id,
                            agent_run_id=workflow_input.agent_run_id,
                            daily_room_url=workflow_input.daily_room_url,
                            daily_room_token=workflow_input.daily_room_token,
                        ),
                    )

                except Exception as e:
                    log.error("Error audio pipeline", error=e)
                    await workflow.step(
                        task_queue="pipeline",
                        function=daily_delete_room,
                        function_input=DailyDeleteRoomInput(
                            room_name=workflow_input.agent_run_id,
                        ),
                    )

                await workflow.step(
                    task_queue="pipeline",
                    function=daily_delete_room,
                    function_input=DailyDeleteRoomInput(
                        room_name=workflow_input.agent_run_id,
                    ),
                )

                await workflow.step(
                    task_queue="pipeline",
                    function=send_agent_event,
                    function_input=SendAgentEventInput(
                        event_name="end",
                        agent_id=workflow_input.agent_id,
                        run_id=workflow_input.agent_run_id,
                    ),
                )

        except Exception as e:
            error_message = f"Error during pipecat_pipeline: {e}"
            raise NonRetryableError(error_message) from e
        else:
            log.info("Pipecat pipeline done")

            return True
