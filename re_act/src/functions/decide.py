import os
from dataclasses import dataclass

from dotenv import load_dotenv
from openai import OpenAI
from restack_ai.function import FunctionFailure, function, log

load_dotenv()


def raise_missing_api_key_error() -> None:
    error_message = "OPENAI_API_KEY is not set"
    log.error(error_message)
    raise FunctionFailure(error_message, non_retryable=True)


@dataclass
class DecideInput:
    email: str
    current_accepted_applicants_count: int


@function.defn()
async def decide(decide_input: DecideInput) -> str:
    try:
        if os.environ.get("OPENAI_API_KEY") is None:
            raise_missing_api_key_error()

        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        tools = [
            {
                "type": "function",
                "function": {
                    "name": "accept_applicant",
                    "description": "Accept the applicant",
                    "parameters": {},
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "reject_applicant",
                    "description": "Reject the applicant",
                    "parameters": {},
                },
            },
        ]

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """
                    You are a helpful assistant for event registration that
                    decides if the applicant should be accepted or rejected.
                    """,
                },
                {
                    "role": "user",
                    "content": f"""
                    The event is called "Restack AI Summit 2025"
                    Restack is the main sponsor of the event.
                    The applicant has the following email:
                    {decide_input.email}
                    The current number of accepted applicants is:
                    {decide_input.current_accepted_applicants_count}
                    The maximum number of accepted applicants is: 10

                    Decide if the applicant should be accepted or rejected.
                    """,
                },
            ],
            tools=tools,
        )

        return response.choices[0].message.tool_calls
    except Exception as e:
        error_message = "Failed to decide"
        log.error(error_message, error=e)
        raise FunctionFailure(error_message, non_retryable=True) from e
