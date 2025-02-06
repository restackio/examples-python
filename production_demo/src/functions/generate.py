from openai import OpenAI, OpenAIError
from pydantic import BaseModel
from restack_ai.function import FunctionFailure, function, log


class GenerateInput(BaseModel):
    prompt: str


@function.defn()
async def llm_generate(generate_input: GenerateInput) -> str:
    try:
        client = OpenAI(base_url="http://192.168.205.1:1234/v1/", api_key="llmstudio")
    except OpenAIError as e:
        error_message = "Failed to create OpenAI client"
        log.error(error_message, error=e)
        raise FunctionFailure(error_message, non_retryable=True) from e
    except Exception as e:
        error_message = "Failed to create LLM Studio client"
        log.error(error_message, error=e)
        raise FunctionFailure(error_message, non_retryable=True) from e

    try:
        response = client.chat.completions.create(
            model="llama-3.2-3b-instruct",
            messages=[
                {
                    "role": "user",
                    "content": generate_input.prompt,
                },
            ],
            temperature=0.5,
        )

    except OpenAIError as e:
        error_message = "OpenAI Error"
        log.error(error_message, error=e)
        raise FunctionFailure(error_message, non_retryable=True) from e
    except Exception as e:
        error_message = "Failed to generate"
        log.error(error_message, error=e)
        raise FunctionFailure(error_message, non_retryable=True) from e

    return response.choices[0].message.content
