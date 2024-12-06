from restack_ai.function import function, FunctionFailure, log
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

@function.defn()
async def openai_joke():

    log.info(f"Generating joke")
    try:
        client = OpenAI(base_url="http://192.168.4.142:1234/v1/",api_key="llmstudio")
    except Exception as e:
        log.error(f"Failed to create OpenAI client {e}")
        raise FunctionFailure(f"Failed to create OpenAI client {e}", non_retryable=True) from e

    try:
        response = client.chat.completions.create(
            model="mlx-community/Meta-Llama-3.1-8B-Instruct-4bit",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that tells jokes."
                },
                {
                    "role": "user",
                    "content": f"Generate a random joke in max 20 words."
                }
            ],
            temperature=0.5,
        )
    
    except Exception as e:
        log.error(f"Failed to generate joke {e}")
    
    return response.choices[0].message.content

