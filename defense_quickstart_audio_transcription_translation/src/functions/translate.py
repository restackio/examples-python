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
        if not os.environ.get("OPENBABYLON_API_URL"):
            raise Exception("OPENBABYLON_API_URL is not set")
        

        client = OpenAI(api_key='openbabylon',base_url=os.environ.get("OPENBABYLON_API_URL"))

        messages = []
        if input.user_prompt:
            messages.append({"role": "user", "content": input.user_prompt})
        print(messages)
        response = client.chat.completions.create(
            model="orpo-mistral-v0.3-ua-tokV2-focus-10B-low-lr-1epoch-aux-merged-1ep",
            messages=messages,
            temperature=0.0
        )
        log.info("translate function completed", response=response)
        return response.choices[0].message
    except Exception as e:
        log.error("translate function failed", error=e)
        raise e
