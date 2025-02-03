import os
from dataclasses import dataclass

import sendgrid
from dotenv import load_dotenv
from restack_ai.function import FunctionFailure, function
from sendgrid.helpers.mail import Mail

load_dotenv()

@dataclass
class SendEmailInput:
    text: str
    subject: str
    to: str

@function.defn()
async def send_email(input: SendEmailInput) -> None:
    from_email = os.getenv("FROM_EMAIL")

    if not from_email:
        raise FunctionFailure("FROM_EMAIL is not set", non_retryable=True)

    sendgrid_api_key = os.getenv("SENDGRID_API_KEY")

    if not sendgrid_api_key:
        raise FunctionFailure("SENDGRID_API_KEY is not set", non_retryable=True)


    message = Mail(
        from_email=from_email,
        to_emails=input.to,
        subject=input.subject,
        plain_text_content=input.text,
    )

    try:
        sg = sendgrid.SendGridAPIClient(sendgrid_api_key)
        sg.send(message)
    except Exception:
        raise FunctionFailure("Failed to send email", non_retryable=False)
