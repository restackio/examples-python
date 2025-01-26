from restack_ai.workflow import workflow, import_functions, log, RetryPolicy
from datetime import timedelta
from pydantic import BaseModel

with import_functions():
    from src.functions.openai_chat_completion import openai_chat_completion, OpenAIInputParams, OpenAIOutputParams

class WorkflowInputParams(BaseModel):
    user_content: str = "What is restack?"
    system_content: str = "You are a helpful assistant"

class WorkflowOutputParams(BaseModel):
    message: str

@workflow.defn()
class ChatbotWorkflow:
    @workflow.run
    async def run(self, input: WorkflowInputParams) -> WorkflowOutputParams:
        log.info("ChatbotWorkflow started", input=input)
        
        chat_completion = await workflow.step(
            openai_chat_completion,
            OpenAIInputParams(
                user_content=input.user_content,
                system_content=input.system_content,
                base_url="https://ai.restack.io",
                model="restack-r1"
            ),
            start_to_close_timeout=timedelta(seconds=120),
            retry_policy=RetryPolicy(
                maximum_attempts=1
            )
        )
        log.info("ChatbotWorkflow completed", chat_completion=chat_completion)
        return WorkflowOutputParams(message=chat_completion.message)
