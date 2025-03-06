from restack_ai.function import function, log, FunctionFailure
from dataclasses import dataclass
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

tries = 0

@dataclass
class GenerateEmailInput:
    email_context: str
    simulate_failure: bool = False

@function.defn()
async def generate_email_content(input: GenerateEmailInput):
    global tries

    if input.simulate_failure and tries == 0:
        tries += 1
        raise FunctionFailure("Simulated failure", non_retryable=False)
    
    if (os.environ.get("OPENAI_API_KEY") is None):
        raise FunctionFailure("OPENAI_API_KEY is not set", non_retryable=True)
    
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that generates short emails based on the provided context."
            },
            {
                "role": "user",
                "content": f"Generate a short email based on the following context: {input.email_context}"
            }
        ],
        max_tokens=150
    )
    
    return response.choices[0].message.content

