import sendgrid
from sendgrid.helpers.mail import Mail
from restack_ai.function import function, log, FunctionFailure
from dotenv import load_dotenv
import os
from dataclasses import dataclass

load_dotenv()

@dataclass
class SendEmailInput:
    subject: str
    body: str

@function.defn()
async def send_email(input: SendEmailInput):
    from_email = os.environ.get("FROM_EMAIL")

    if not from_email:
        raise FunctionFailure('FROM_EMAIL is not set', non_retryable=True)
    
    sendgrid_api_key = os.getenv('SENDGRID_API_KEY')

    if not sendgrid_api_key:
        raise FunctionFailure('SENDGRID_API_KEY is not set', non_retryable=True)
    
    message = Mail(
        from_email=from_email,
        to_emails=from_email,
        subject=input.subject,
        plain_text_content=input.body
    )

    try:
        sg = sendgrid.SendGridAPIClient(api_key=sendgrid_api_key)
        sg.send(message)
    except Exception as e:
        log.error("Failed to send email", error=e)
        raise FunctionFailure("Failed to send email", non_retryable=True)
