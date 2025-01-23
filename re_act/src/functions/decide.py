from restack_ai.function import function, log, FunctionFailure
from dataclasses import dataclass
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class DecideInput:
    email: str
    current_accepted_applicants_count: int

@function.defn()
async def decide(input: DecideInput):
    try:
        if (os.environ.get("OPENAI_API_KEY") is None):
                raise FunctionFailure("OPENAI_API_KEY is not set", non_retryable=True)
            
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        tools = [
            {
                "type": "function",
                "function": {
                    "name": "accept_applicant",
                    "description": "Accept the applicant",
                    "parameters": {}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "reject_applicant",
                    "description": "Reject the applicant",
                    "parameters": {}
                }
            }
        ]

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": f"""
                    You are a helpful assistant for event registration that decides if the applicant should be accepted or rejected.
                    """
                },
                {
                    "role": "user",
                    "content": f"""
                    The event is called "Restack AI Summit 2025"
                    Restack is the main sponsor of the event.
                    The applicant has the following email: {input.email}
                    The current number of accepted applicants is: {input.current_accepted_applicants_count}
                    The maximum number of accepted applicants is: 10

                    Decide if the applicant should be accepted or rejected.
                    """,
                }
            ],
            tools=tools
        )
        
        return response.choices[0].message.tool_calls
    except Exception as e:
        log.error("Failed to decide", error=e)
        raise FunctionFailure("Failed to decide", non_retryable=True)

