from restack_ai.function import function, log, FunctionFailure
from dataclasses import dataclass
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class GenerateEmailInput:
    email_context: str

@function.defn()
async def generate_email_content(input: GenerateEmailInput):

    try:
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": f"""
                    You are a helpful assistant that generates short emails based on the provided context.
                    """
                },
                {
                    "role": "user",
                    "content": f"""Generate a short email based on the following context: {input.email_context}
                    """
                }
            ],
            max_tokens=150
        )
        
        return response.choices[0].message.content
    except Exception as e:
        log.error("Failed to generate email content", error=e)
        raise FunctionFailure("Failed to generate email content", non_retryable=True)

