from openai import OpenAI, OpenAIError
from pydantic import BaseModel
from restack_ai.function import FunctionFailure, function, log


class EvaluateInput(BaseModel):
    generated_text: str


@function.defn()
async def llm_evaluate(evaluate_input: EvaluateInput) -> str:
    try:
        client = OpenAI(base_url="http://192.168.205.1:1234/v1/", api_key="llmstudio")
    except OpenAIError as e:
        error_message = "Failed to create OpenAI client"
        log.error(error_message, error=e)
        raise FunctionFailure(error_message, non_retryable=True) from e
    except Exception as e:
        error_message = "Failed to create LLM client"
        log.error(error_message, error=e)
        raise FunctionFailure(error_message, non_retryable=True) from e

    prompt = (
        f"Evaluate the following joke for humor, creativity, and originality. "
        f"Provide a score out of 10 for each category for your score.\n\n"
        f"Joke: {evaluate_input.generated_text}\n\n"
        f"Response format:\n"
        f"Humor: [score]/10"
        f"Creativity: [score]/10"
        f"Originality: [score]/10"
        f"Average score: [score]/10"
        f"Only answer with the scores"
    )

    try:
        response = client.chat.completions.create(
            model="llama-3.2-3b-instruct",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
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
