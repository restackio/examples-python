from restack_ai.function import function, FunctionFailure, log
from openai import OpenAI
from pydantic import BaseModel

class EvaluateInput(BaseModel):
    generated_text: str

@function.defn()
async def llm_evaluate(input: EvaluateInput) -> str:
    try:
        client = OpenAI(base_url="http://192.168.205.1:1234/v1/",api_key="llmstudio")
    except Exception as e:
        log.error(f"Failed to create LLM client {e}")
        raise FunctionFailure(f"Failed to create OpenAI client {e}", non_retryable=True) from e

    prompt = (
        f"Evaluate the following joke for humor, creativity, and originality. "
        f"Provide a score out of 10 for each category for your score.\n\n"
        f"Joke: {input.generated_text}\n\n"
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
                    "content": prompt
                }
            ],
            temperature=0.5,
        )
    
    except Exception as e:
        log.error(f"Failed to generate {e}")
    
    return response.choices[0].message.content