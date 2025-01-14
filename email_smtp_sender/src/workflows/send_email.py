from restack_ai.workflow import workflow, import_functions, log, RetryPolicy
from datetime import timedelta
from pydantic import BaseModel, Field

with import_functions():
    from src.functions.smtp_send_email import smtp_send_email, SendEmailInput

class WorkflowInputParams(BaseModel):
    body: str = Field(default="SMTP Email Body Content")
    subject: str = Field(default="SMTP Email Subject")
    to_email: str = Field(default="SMTP Email Recipient Address")

@workflow.defn()
class SendEmailWorkflow:
    @workflow.run
    async def run(self, input: WorkflowInputParams):
        
        emailState = await workflow.step(
            smtp_send_email,
            SendEmailInput(
                body=input.body,
                subject=input.subject,
                to_email=input.to_email,
            ),
            start_to_close_timeout=timedelta(seconds=15),
            retry_policy=RetryPolicy(maximum_attempts=1)
        )

        return emailState
