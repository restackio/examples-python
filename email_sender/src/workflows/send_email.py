from dataclasses import dataclass
from datetime import timedelta

from restack_ai.workflow import RetryPolicy, import_functions, log, workflow

with import_functions():
    from src.functions.generate_email_content import (
        GenerateEmailInput,
        generate_email_content,
    )
    from src.functions.send_email import SendEmailInput, send_email


@dataclass
class WorkflowInputParams:
    email_context: str
    subject: str
    to: str
    simulate_failure: bool = False


@workflow.defn()
class SendEmailWorkflow:
    @workflow.run
    async def run(self, workflow_input: WorkflowInputParams) -> str:
        log.info("SendEmailWorkflow started", input=workflow_input)

        text = await workflow.step(
            generate_email_content,
            GenerateEmailInput(
                email_context=workflow_input.email_context,
                simulate_failure=workflow_input.simulate_failure,
            ),
            retry_policy=RetryPolicy(
                initial_interval=timedelta(seconds=10),
                backoff_coefficient=1,
            ),
        )

        await workflow.step(
            send_email,
            SendEmailInput(
                text=text,
                subject=workflow_input.subject,
                to=workflow_input.to,
            ),
            start_to_close_timeout=timedelta(seconds=120),
        )

        return "Email sent successfully"
