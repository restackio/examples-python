from restack_ai.function import function
from restack_google_gemini import (
    gemini_get_history,
    GeminiGetHistoryInput,
    gemini_start_chat,
    GeminiStartChatInput,
    gemini_send_message,
    GeminiSendMessageInput
)
from typing import Any
from dataclasses import dataclass
import os
import json

from src.functions.util import read_repostitory_scan

@dataclass
class FunctionInputParams:
    user_content: str
    chat_history: list[Any]
    repo_contents_file_path: str | None = None
    
@dataclass
class FilesToCreateOrUpdate:
    file_path: str
    content: str

@dataclass
class GeminiGenerateContentResponse:
    files_to_create_or_update: list[FilesToCreateOrUpdate]

@dataclass
class FunctionOutputParams:
    files_to_create_or_update: list[FilesToCreateOrUpdate]
    chat_history: list[Any]


@function.defn(name="GenerateSolution")
async def generate_solution(input: FunctionInputParams) -> FunctionOutputParams:
    """Generates solution files based on user input and repository context.

    Uses Gemini AI to analyze the repository contents and user requirements,
    then generates or updates necessary files with complete content.

    Args:
        input (FunctionInputParams): Contains user_content, chat_history, and optional repo_contents_file_path

    Returns:
        FunctionOutputParams: Contains list of files to create/update and updated chat history
    """

    chat_rule = """
        Generate a solution following these specific guidelines:

        1. File Structure Format:
           Return a list of files to be created/updated, where each file contains:
           - file_path: Absolute path to the file
           - content: Complete file contents

        2. File Path Rules:
           - ALWAYS start paths with forward slash (/)
           - Paths must be absolute from repository root
           - Format: /Users/{username}/Code/github.com/{org}/{repo}/path/to/file.ext
           - Remove any leading/trailing whitespace
           - Use forward slashes (/) for path separation
           - Do not include quotes around paths
           - Examples:
             * /Users/username/Code/github.com/organization/project/src/components/Button.tsx
             * /Users/username/Code/github.com/organization/project/src/utils/helpers.js
             * /Users/username/Code/github.com/organization/project/tests/unit/auth.test.ts

        3. Content Rules:
           - For new files: Provide complete, well-structured content
           - For existing files: Include the entire updated file content
           - Maintain proper indentation and formatting
           - Include necessary imports and dependencies
           - Add appropriate comments for complex logic

        4. Code Style:
           - Follow the existing project's coding conventions
           - Use consistent naming conventions
           - Maintain proper spacing and line breaks
           - Include error handling where appropriate

        IMPORTANT:
        - CRITICAL: Every file_path MUST start with /Users/{username}/Code/github.com/{org}/{repo}/
        - Always analyze if a file needs creation or update
        - Return complete file contents, not just changes
        - Response must be valid JSON matching the specified schema
        - Preserve existing code structure when updating files
    """

    if len(input.chat_history) == 0:
        content = read_repostitory_scan(input.repo_contents_file_path)
        prompt = f"This is my code repository:\n{content}\n\nThis is my new current task:\n{input.user_content}\n\n{chat_rule}"
    else:
        prompt = f"This is my feedback:\n{input.user_content}\n\n{chat_rule}"

    
    gemini_chat = gemini_start_chat(
        GeminiStartChatInput(
            model="gemini-1.5-flash",
            api_key=os.environ.get("GEMINI_API_KEY"),
            generation_config={
                "response_mime_type": "application/json",
                "response_schema": GeminiGenerateContentResponse
            },
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
        
    return FunctionOutputParams(
        files_to_create_or_update=json.loads(gemini_send_message_response.text)['files_to_create_or_update'],
        chat_history=gemini_get_history_response
    )

