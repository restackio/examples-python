import os
from dataclasses import dataclass

from dotenv import load_dotenv
from openai import OpenAI
from restack_ai.function import FunctionFailure, function, log

load_dotenv()

tries = 0


@dataclass
class GenerateEmailInput:
    email_context: str
    simulate_failure: bool = False


@function.defn()
async def generate_email_content(generate_email_input: GenerateEmailInput) -> str:
    global tries  # noqa: PLW0603

    if generate_email_input.simulate_failure and tries == 0:
        tries += 1
        error_message = "Simulated failure"
        log.error(error_message)
        raise FunctionFailure(error_message, non_retryable=False)

    if os.environ.get("OPENAI_API_KEY") is None:
        error_message = "OPENAI_API_KEY is not set"
        log.error(error_message)
        raise FunctionFailure(error_message, non_retryable=True)

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": """
                You are a helpful assistant that generates short emails based
                on the provided context.
                The email should be short and to the point.
                """,
            },
            {
                "role": "user",
                "content": f"""
                Generate a short email based on the following context:
                {input.email_context}
                """,
            },
        ],
        max_tokens=150,
    )

    return response.choices[0].message.content
