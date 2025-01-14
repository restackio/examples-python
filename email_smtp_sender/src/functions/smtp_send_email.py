import os
from restack_ai.function import function, FunctionFailure, log
from dataclasses import dataclass
from dotenv import load_dotenv

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import json

load_dotenv()

@dataclass
class SendEmailInput:
    to_email: str
    subject: str
    body: str

@function.defn()
async def smtp_send_email(input: SendEmailInput):

    config = load_smtp_config()

    # Verify input.to_email is a valid email address - quick n dirty
    if not "@" in input.to_email:
        raise FunctionFailure("SMTPSendEmail: input.to_email not valid email", non_retryable=True)

    # Create message
    message = MIMEMultipart()
    message["From"] = config.get("SMTP_FROM_EMAIL")
    message["To"] = input.to_email
    message["Subject"] = input.subject

    # Add body
    message.attach(MIMEText(input.body, "plain"))

    try:
        # Create SMTP session
        with smtplib.SMTP(config.get("SMTP_SERVER"), config.get("SMTP_PORT")) as server:
            server.starttls()
            server.login(config.get("SMTP_USERNAME"), config.get("SMTP_PASSWORD"))
            
            # Send email
            print(f"Sending email to {input.to_email}")
            server.send_message(message)
            print("Email sent successfully")

            return f"Email sent successfully to {input.to_email}"

    except Exception as e:
        log.error("Failed to send email", error=e)

        errorMessage = json.dumps({"error": f"Failed to send email {e}"})
        raise FunctionFailure(errorMessage, non_retryable=False)


def load_smtp_config():
    """Validates that we have all essential environment variables set; raises an exception if not."""
    
    required_vars = {
        "SMTP_SERVER": os.getenv("SMTP_SERVER"),
        "SMTP_PORT": os.getenv("SMTP_PORT"),
        "SMTP_USERNAME": os.getenv("SMTP_USERNAME"),
        "SMTP_PASSWORD": os.getenv("SMTP_PASSWORD"),
        "SMTP_FROM_EMAIL": os.getenv("SMTP_FROM_EMAIL"),
    }

    missing = [var for var, value in required_vars.items() if not value]

    if missing:
        raise FunctionFailure(f"Missing required environment variables: {missing}", non_retryable=True)

    return required_vars