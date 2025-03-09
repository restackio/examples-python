from datetime import timedelta
from typing import Any

from pydantic import BaseModel
from restack_ai.agent import (
    NonRetryableError,
    RetryPolicy,
    agent,
    agent_info,
    import_functions,
    log,
    uuid,
)

from src.workflows.logic import LogicWorkflow, LogicWorkflowInput

with import_functions():
    from src.functions.livekit_call import (
        LivekitCallInput,
        livekit_call,
    )
    from src.functions.livekit_create_room import (
        livekit_create_room,
    )
    from src.functions.livekit_delete_room import (
        livekit_delete_room,
    )
    from src.functions.livekit_dispatch import (
        LivekitDispatchInput,
        livekit_dispatch,
    )
    from src.functions.livekit_outbound_trunk import (
        livekit_outbound_trunk,
    )
    from src.functions.livekit_send_data import (
        LivekitSendDataInput,
        SendDataResponse,
        livekit_send_data,
    )
    from src.functions.livekit_start_recording import (
        EgressInfo,
        LivekitStartRecordingInput,
        livekit_start_recording,
    )
    from src.functions.livekit_token import (
        LivekitTokenInput,
        livekit_token,
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


class MessagesEvent(BaseModel):
    messages: list[Message]


class EndEvent(BaseModel):
    end: bool


class CallInput(BaseModel):
    phone_number: str


class ContextEvent(BaseModel):
    context: str


class PipelineMetricsEvent(BaseModel):
    metrics: Any
    latencies: str

class AgentTwilioInput(BaseModel):
    phone_number: str | None = None

class AgentTwilioOutput(BaseModel):
    recording_url: str
    livekit_room_id: str
    messages: list[Message]
    context: str


@agent.defn()
class AgentTwilio:
    def __init__(self) -> None:
        self.end = False
        self.messages = []
        self.context = ""
        self.room_id = ""

    @agent.event
    async def messages(
        self, messages_event: MessagesEvent
    ) -> list[Message]:
        log.info(f"Received message: {messages_event.messages}")
        self.messages.extend(messages_event.messages)

        try:
            await agent.child_start(
                workflow=LogicWorkflow,
                workflow_id=f"{uuid()}-logic",
                workflow_input=LogicWorkflowInput(
                    messages=self.messages,
                    room_id=self.room_id,
                    context=str(self.context),
                ),
            )

            fast_response = await agent.step(
                function=llm_talk,
                function_input=LlmTalkInput(
                    messages=self.messages[-3:],
                    context=str(self.context),
                    mode="default",
                ),
                start_to_close_timeout=timedelta(seconds=3),
                retry_policy=RetryPolicy(
                    initial_interval=timedelta(seconds=1),
                    maximum_attempts=1,
                    maximum_interval=timedelta(seconds=5),
                ),
            )

            self.messages.append(
                Message(role="assistant", content=fast_response)
            )
            return self.messages
        except Exception as e:
            error_message = f"Error during messages: {e}"
            raise NonRetryableError(error_message) from e

    @agent.event
    async def call(self, call_input: CallInput) -> None:
        log.info("Call", call_input=call_input)
        phone_number = call_input.phone_number
        agent_name = agent_info().workflow_type
        agent_id = agent_info().workflow_id
        run_id = agent_info().run_id
        try:
            sip_trunk_id = await agent.step(
                function=livekit_outbound_trunk
            )
            await agent.step(
                function=livekit_call,
                function_input=LivekitCallInput(
                    sip_trunk_id=sip_trunk_id,
                    phone_number=phone_number,
                    room_id=self.room_id,
                    agent_name=agent_name,
                    agent_id=agent_id,
                    run_id=run_id,
                ),
            )
        except Exception as e:
            error_message = (
                f"Error during livekit_outbound_trunk: {e}"
            )
            raise NonRetryableError(error_message) from e

    @agent.event
    async def say(self, say: str) -> SendDataResponse:
        log.info("Received say")
        return await agent.step(
            function=livekit_send_data,
            function_input=LivekitSendDataInput(text=say),
        )

    @agent.event
    async def end(self, end: EndEvent) -> EndEvent:
        log.info("Received end")
        await agent.step(
            function=livekit_send_data,
            function_input=LivekitSendDataInput(
                room_id=self.room_id,
                text="Thank you for calling restack. Goodbye!",
            ),
        )
        await agent.sleep(8)
        await agent.step(function=livekit_delete_room)

        self.end = True
        return end

    @agent.event
    async def context(self, context: ContextEvent) -> str:
        log.info("Received context")
        self.context = context.context
        return self.context

    @agent.event
    async def pipeline_metrics(
        self, pipeline_metrics: PipelineMetricsEvent
    ) -> PipelineMetricsEvent:
        log.info(
            "Received pipeline metrics",
            pipeline_metrics=pipeline_metrics,
        )
        return pipeline_metrics

    @agent.run
    async def run(self, agent_input: AgentTwilioInput) -> AgentTwilioOutput:
        try:
            room = await agent.step(function=livekit_create_room)
            self.room_id = room.name
            await agent.step(
                function=livekit_token,
                function_input=LivekitTokenInput(
                    room_id=self.room_id
                ),
            )
            recording: EgressInfo = await agent.step(
                function=livekit_start_recording,
                function_input=LivekitStartRecordingInput(
                    room_id=self.room_id
                ),
            )
            await agent.step(
                function=livekit_dispatch,
                function_input=LivekitDispatchInput(
                    room_id=self.room_id
                ),
            )

            if agent_input.phone_number:
                
                agent_id = agent_info().workflow_id
                run_id = agent_info().run_id

                await agent.step(
                    function=send_agent_event,
                    function_input=SendAgentEventInput(
                        event_name="call",
                        agent_id=agent_id,
                        run_id=run_id,
                        event_input={
                            "phone_number": agent_input.phone_number,
                        },
                    ),
                )

        except Exception as e:
            error_message = f"Error during agent run: {e}"
            raise NonRetryableError(error_message) from e
        else:
            await agent.condition(lambda: self.end)

            recording_url = f"https://storage.googleapis.com/{recording.room_composite.file_outputs[0].gcp.bucket}/{recording.room_composite.file_outputs[0].filepath}"

            return AgentTwilioOutput(
                recording_url=recording_url,
                livekit_room_id=self.room_id,
                messages=self.messages,
                context=self.context,
            )
