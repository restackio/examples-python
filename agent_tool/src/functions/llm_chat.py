from restack_ai.function import function, log
from openai import OpenAI, pydantic_function_tool
from openai.types.chat.chat_completion import ChatCompletion
from openai.types.chat.chat_completion_message_tool_call import ChatCompletionMessageToolCall
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Literal, Optional, List
from src.workflows.workflow import SalesWorkflow, SalesWorkflowInput

load_dotenv()

class Message(BaseModel):
    role: Literal["system", "user", "assistant", "tool"]
    content: str
    tool_call_id: Optional[str] = None
    tool_calls: Optional[List[ChatCompletionMessageToolCall]] = None

class LlmChatInput(BaseModel):
    system_content: Optional[str] = None
    model: Optional[str] = None
    messages: Optional[List[Message]] = None

@function.defn()
async def llm_chat(input: LlmChatInput) -> ChatCompletion:
    try:
        log.info("llm_chat function started", input=input)
        client = OpenAI(base_url="https://ai.restack.io", api_key=os.environ.get("RESTACK_API_KEY"))


        tools = [pydantic_function_tool(
            model=SalesWorkflowInput,
            name=SalesWorkflow.__name__,
            description="Lookup sales for a given category"
        )]

        log.info("pydantic_function_tool", tools=tools)

        if input.system_content:
            input.messages.append(Message(role="system", content=input.system_content or ""))

        response = client.chat.completions.create(
            model=input.model or "restack-c1",
            messages=input.messages,
            tools=tools,
        )
        return response
    except Exception as e:
        log.error("llm_chat function failed", error=e)
        raise e
