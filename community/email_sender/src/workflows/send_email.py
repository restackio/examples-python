from restack_ai.workflow import workflow, import_functions, log, RetryPolicy
from dataclasses import dataclass
from datetime import timedelta

with import_functions():
    from src.functions.send_email import send_email, SendEmailInput
    from src.functions.generate_email_content import generate_email_content, GenerateEmailInput

@dataclass
class WorkflowInputParams:
    email_context: str
    subject: str
    to: str
    simulate_failure: bool = False

@workflow.defn()
class SendEmailWorkflow:
    @workflow.run
    async def run(self, input: WorkflowInputParams):
        log.info("SendEmailWorkflow started", input=input)

        text = await workflow.step(
            function=generate_email_content,
            function_input=GenerateEmailInput(
                email_context=input.email_context,
                simulate_failure=input.simulate_failure,
            ),
            retry_policy=RetryPolicy(
                initial_interval=timedelta(seconds=10),
                backoff_coefficient=1,
            ),
        )

        await workflow.step(
            function=send_email,
            function_input=SendEmailInput(
                text=text,
                subject=input.subject,
                to=input.to,
            ),
            start_to_close_timeout=timedelta(seconds=120)
        )

        return 'Email sent successfully'
