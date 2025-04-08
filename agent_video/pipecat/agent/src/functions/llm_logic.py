import os
from typing import Literal

from openai import AsyncOpenAI
from pydantic import BaseModel
from restack_ai.function import NonRetryableError, function

from src.functions.llm_talk import Message


class LlmLogicResponse(BaseModel):
    """Structured AI decision output used to interrupt conversations."""

    action: Literal["interrupt", "update_context", "end_call"]
    reason: str
    updated_context: str


class LlmLogicInput(BaseModel):
    messages: list[Message]
    documentation: str
    reasoning_prompt: str | None = None


@function.defn()
async def llm_logic(
    function_input: LlmLogicInput,
) -> LlmLogicResponse:
    try:
        client = AsyncOpenAI(
            api_key=os.environ.get("OPENAI_API_KEY")
        )

        if function_input.reasoning_prompt:
            system_prompt = (
                function_input.reasoning_prompt
                + f"Restack Documentation: {function_input.documentation}"
            )
        else:
            system_prompt = (
                "Analyze the developer's questions and determine if an interruption is needed. "
                "For example, to ask a follow up question and keep the conversation going. "
                "Use the Restack documentation for accurate answers. "
                "Track what the developer has learned and update their belief state."
                f"Restack Documentation: {function_input.documentation}"
            )

        response = await client.beta.chat.completions.parse(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                *function_input.messages,
            ],
            response_format=LlmLogicResponse,
        )

        return response.choices[0].message.parsed

    except Exception as e:
        raise NonRetryableError(f"llm_slow failed: {e}") from e
