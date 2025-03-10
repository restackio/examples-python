from datetime import timedelta

from pydantic import BaseModel
from restack_ai.workflow import (
    NonRetryableError,
    import_functions,
    log,
    workflow,
    workflow_info,
)

with import_functions():
    from src.functions.context_docs import context_docs
    from src.functions.livekit_send_data import (
        LivekitSendDataInput,
        livekit_send_data,
    )
    from src.functions.llm_logic import (
        LlmLogicInput,
        LlmLogicResponse,
        llm_logic,
    )
    from src.functions.llm_talk import (
        LlmTalkInput,
        Message,
        llm_talk,
    )
    from src.functions.send_agent_event import (
        SendAgentEventInput,
        send_agent_event,
    )


class LogicWorkflowInput(BaseModel):
    messages: list[Message]
    room_id: str
    context: str


class LogicWorkflowOutput(BaseModel):
    result: str


@workflow.defn()
class LogicWorkflow:
    @workflow.run
    async def run(
        self, workflow_input: LogicWorkflowInput
    ) -> str:
        context = workflow_input.context

        parent_agent_id = workflow_info().parent.workflow_id
        parent_agent_run_id = workflow_info().parent.run_id

        log.info("LogicWorkflow started")
        try:
            documentation = await workflow.step(
                function=context_docs
            )

            slow_response: LlmLogicResponse = await workflow.step(
                function=llm_logic,
                function_input=LlmLogicInput(
                    messages=[
                        msg.model_dump()
                        for msg in workflow_input.messages
                    ],
                    documentation=documentation,
                ),
                start_to_close_timeout=timedelta(seconds=60),
            )

            log.info(f"Slow response: {slow_response}")

            context = slow_response.updated_context

            await workflow.step(
                function=send_agent_event,
                function_input=SendAgentEventInput(
                    event_name="context",
                    agent_id=parent_agent_id,
                    run_id=parent_agent_run_id,
                    event_input={"context": str(context)},
                ),
            )

            if slow_response.action == "interrupt":
                interrupt_response = await workflow.step(
                    function=llm_talk,
                    function_input=LlmTalkInput(
                        messages=[
                            Message(
                                role="system",
                                content=slow_response.reason,
                            )
                        ],
                        context=str(context),
                        mode="interrupt",
                        stream=False,
                    ),
                    start_to_close_timeout=timedelta(seconds=3),
                )

                await workflow.step(
                    function=livekit_send_data,
                    function_input=LivekitSendDataInput(
                        room_id=parent_agent_run_id,
                        text=interrupt_response,
                    ),
                )

            if slow_response.action == "end_call":
                goodbye_message = await workflow.step(
                    function=llm_talk,
                    function_input=LlmTalkInput(
                        messages=[
                            Message(
                                role="system",
                                content="Say goodbye to the user by providing a unique and short message based on context.",
                            )
                        ],
                        context=str(context),
                        mode="interrupt",
                        stream=False,
                    ),
                    start_to_close_timeout=timedelta(seconds=3),
                )

                log.info(f"Goodbye message: {goodbye_message}")

                await workflow.step(
                    function=livekit_send_data,
                    function_input=LivekitSendDataInput(
                        room_id=parent_agent_run_id,
                        text=goodbye_message,
                    ),
                )

                await workflow.sleep(1)

                await workflow.step(
                    function=send_agent_event,
                    function_input=SendAgentEventInput(
                        event_name="end",
                        agent_id=parent_agent_id,
                        run_id=parent_agent_run_id,
                        event_input={"end": True},
                    ),
                )

        except Exception as e:
            error_message = f"Error during welcome: {e}"
            raise NonRetryableError(error_message) from e
        else:
            log.info(
                "LogicWorkflow completed", context=str(context)
            )
            return str(context)
