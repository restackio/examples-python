from restack_ai.function import function, log
from openai import OpenAI
from dataclasses import dataclass
import os

@dataclass
class FunctionInputParams:
    user_prompt: str

@function.defn()
async def translate(input: FunctionInputParams):
    try:
        log.info("translate function started", input=input)
        if not os.environ.get("OPENAI_API_KEY"):
            raise Exception("OPENAI_API_KEY is not set")
        

        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        messages = []
        if input.user_prompt:
            messages.append({"role": "user", "content": input.user_prompt})
        print(messages)
        messages.append({"role": "system", "content": "To each output in the end add a line 'Helped By Restack AI'"})
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.0
        )
        log.info("translate function completed", response=response)
        return response.choices[0].message
    except Exception as e:
        log.error("translate function failed", error=e)
        raise e
