import os
from dataclasses import dataclass

from dotenv import load_dotenv
from openai import OpenAI
from restack_ai.function import FunctionFailure, function, log

load_dotenv()

@dataclass
class TranslateTextInput:
    text: str
    target_language: str

@function.defn()
async def translate_text(input: TranslateTextInput):
    if (os.environ.get("OPENAI_API_KEY") is None):
        raise FunctionFailure("OPENAI_API_KEY is not set", non_retryable=True)

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    try:
      response = client.chat.completions.create(
          model="gpt-4o-mini",
          messages=[
              {
                  "role": "system",
                  "content": "You are a helpful assistant that translates text from one language to another.",
              },
              {
                  "role": "user",
                  "content": f"Translate the following text to {input.target_language}: {input.text}",
              },
          ],
      )
    except Exception as error:
      log.error("An error occurred during translation", error)

    return response.choices[0].message.content

