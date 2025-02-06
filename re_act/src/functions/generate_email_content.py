import os
from dataclasses import dataclass

from dotenv import load_dotenv
from openai import OpenAI
from restack_ai.function import FunctionFailure, function, log

load_dotenv()


@dataclass
class GenerateEmailInput:
    email_context: str


@function.defn()
async def generate_email_content(generate_email_input: GenerateEmailInput) -> str:
    try:
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """
                    You are a helpful assistant that generates short
                    emails based on the provided context.
                    """,
                },
                {
                    "role": "user",
                    "content": f"""Generate a short email based on
                    the following context: {generate_email_input.email_context}
                    """,
                },
            ],
            max_tokens=150,
        )

        return response.choices[0].message.content
    except Exception as e:
        error_message = "Failed to generate email content"
        log.error(error_message, error=e)
        raise FunctionFailure(error_message, non_retryable=True) from e
