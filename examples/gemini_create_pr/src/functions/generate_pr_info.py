from restack_ai.function import function
from typing import Any
from dataclasses import dataclass
from restack_google_gemini import (
    gemini_get_history,
    GeminiGetHistoryInput,
    gemini_start_chat,
    GeminiStartChatInput,
    gemini_send_message,
    GeminiSendMessageInput
)
import os
import json

@dataclass
class FunctionInputParams:
    repo_path: str
    chat_history: list[Any]
    user_content: str | None = None

@dataclass
class PrInfo:
    branch_name: str
    commit_message: str
    pr_title: str

@dataclass
class GeminiGenerateContentResponse:
    pr_info: PrInfo

@dataclass
class FunctionOutputParams:
    pr_info: PrInfo
    chat_history: list[Any]


@function.defn(name="GeneratePrInfo")
async def generate_pr_info(input: FunctionInputParams):
    chat_rule = """
        Generate a PR information for the changes made to the repository using these specific guidelines:

        1. branch_name:
           - Use lowercase letters and hyphens only
           - Start with a category (feat/fix/docs/refactor/test)
           - Keep it concise but descriptive
           - Example: feat-add-user-authentication

        2. commit_message:
           - Follow conventional commits format
           - Start with type(scope): description
           - Use present tense
           - Be specific but concise
           - Example: feat(auth): implement user authentication system

        3. pr_title:
           - Should be clear and descriptive
           - Start with square brackets indicating the type [FEAT], [FIX], etc.
           - Maximum 72 characters
           - Example: [FEAT] Implement user authentication system

        IMPORTANT:
        - Ignore all copyrighted content
        - Never use emojis in the response
        - Keep all responses in plain text without any formatting
        - Ensure each field is properly formatted as a valid JSON string
    """

    prompt = ""
    if input.user_content is None:
        prompt = f"""
        {chat_rule}
        """
    else:
        prompt = f"""
        This is my feedback:
        {input.user_content}

        {chat_rule}
        """

    generation_config = {
        "response_mime_type": "application/json",
        "response_schema": GeminiGenerateContentResponse
    }

    gemini_chat = gemini_start_chat(
        GeminiStartChatInput(
            model="gemini-1.5-flash",
            api_key=os.environ.get("GEMINI_API_KEY"),
            generation_config=generation_config,
            history=input.chat_history
        )
    )

    gemini_send_message_response = gemini_send_message(
            GeminiSendMessageInput(
                user_content=prompt,
                chat=gemini_chat
            )
        )

    gemini_get_history_response = gemini_get_history(
        GeminiGetHistoryInput(
            chat=gemini_chat
        )
    )

    response = json.loads(gemini_send_message_response.text)
    return FunctionOutputParams(
        pr_info=response['pr_info'],
        chat_history=gemini_get_history_response
    )
