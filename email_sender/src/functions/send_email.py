import os
from dataclasses import dataclass

import sendgrid
from dotenv import load_dotenv
from restack_ai.function import FunctionFailure, function, log
from sendgrid.helpers.mail import Mail

load_dotenv()


@dataclass
class SendEmailInput:
    text: str
    subject: str
    to: str


@function.defn()
async def send_email(send_email_input: SendEmailInput) -> None:
    from_email = os.getenv("FROM_EMAIL")

    if not from_email:
        error_message = "FROM_EMAIL is not set"
        log.error(error_message)
        raise FunctionFailure(error_message, non_retryable=True)

    sendgrid_api_key = os.getenv("SENDGRID_API_KEY")

    if not sendgrid_api_key:
        error_message = "SENDGRID_API_KEY is not set"
        log.error(error_message)
        raise FunctionFailure(error_message, non_retryable=True)

    message = Mail(
        from_email=from_email,
        to_emails=send_email_input.to,
        subject=send_email_input.subject,
        plain_text_content=send_email_input.text,
    )

    try:
        sg = sendgrid.SendGridAPIClient(sendgrid_api_key)
        sg.send(message)
    except Exception as e:
        error_message = "Failed to send email"
        log.error(error_message, error=e)
        raise FunctionFailure(error_message, non_retryable=False) from e
