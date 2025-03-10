import os
from typing import Literal

from openai import OpenAI
from pydantic import BaseModel
from restack_ai.function import NonRetryableError, function

class Message(BaseModel):
    role: str
    content: str

class LlmLogicResponse(BaseModel):
    """Structured AI decision output used to interrupt conversations."""

    action: Literal["interrupt", "update_context", "end_call"]
    reason: str
    updated_context: str


class LlmLogicInput(BaseModel):
    messages: list[Message]
    documentation: str


@function.defn()
async def llm_logic(
    function_input: LlmLogicInput,
) -> LlmLogicResponse:
    try:
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        user_messages = [msg for msg in function_input.messages if msg.role == "user"]
        if len(user_messages) == 1:
            voice_mail_detection = "End the call if a voice mail is detected."
        else:
            voice_mail_detection = ""

        response = client.beta.chat.completions.parse(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Analyze the developer's questions and determine if an interruption is needed. "
                        "Use the Restack documentation for accurate answers. "
                        "Track what the developer has learned and update their belief state."
                        f"{voice_mail_detection}"
                        f"Restack Documentation: {function_input.documentation}"
                    ),
                },
                *function_input.messages,
            ],
            response_format=LlmLogicResponse,
        )

        return response.choices[0].message.parsed

    except Exception as e:
        raise NonRetryableError(f"llm_slow failed: {e}") from e
