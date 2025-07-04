from restack_ai.function import function, NonRetryableError, log
from openai import OpenAI

from pydantic import BaseModel

class GenerateInput(BaseModel):
    prompt: str

@function.defn()
async def llm_generate(input: GenerateInput) -> str:

    try:
        client = OpenAI(base_url="http://192.168.178.57:1234/v1/",api_key="llmstudio")
    except Exception as e:
        log.error(f"Failed to create LLM client {e}")
        raise NonRetryableError(message=f"Failed to create OpenAI client {e}") from e

    try:
        response = client.chat.completions.create(
            model="llama-3.2-3b-instruct",
            messages=[
                {
                    "role": "user",
                    "content": input.prompt
                }
            ],
            temperature=0.5,
        )
    
    except Exception as e:
        log.error(f"Failed to generate {e}")
    
    return response.choices[0].message.content

