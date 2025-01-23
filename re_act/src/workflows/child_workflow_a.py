from restack_ai.workflow import workflow, log, import_functions
from datetime import timedelta
from dataclasses import dataclass

with import_functions():
    from src.functions.generate_email_content import generate_email_content, GenerateEmailInput
    from src.functions.send_email import send_email, SendEmailInput

@workflow.defn()
class ChildWorkflowA:
    @workflow.run
    async def run(self, email: str):
        log.info(f"Sending email to {email}")

        text = await workflow.step(
            generate_email_content,
            input=GenerateEmailInput(
                email_context="Application was accepted"
            ),
            start_to_close_timeout=timedelta(seconds=120)
        )

        await workflow.step(
            send_email,
            input=SendEmailInput(
                subject="Restack AI Summit 2025",
                body=text
            ),
            start_to_close_timeout=timedelta(seconds=120)
        )
