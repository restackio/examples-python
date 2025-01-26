from restack_ai.workflow import workflow, import_functions, log, RetryPolicy
from datetime import timedelta
from pydantic import BaseModel

with import_functions():
    from src.functions.openai_chat_completion import openai_chat_completion, OpenAIInputParams, OpenAIOutputParams
    
class ChatHistory(BaseModel):
    messages: list[tuple[OpenAIInputParams, OpenAIOutputParams]]

class ChatInteractionInputParams(BaseModel):
    chat_id: str
    user_content: str
    system_content: str
    chat_history: ChatHistory | None = None

class ChatInteractionOutputParams(BaseModel):
    message: str
    
@workflow.defn()
class ChatInteraction:
    @workflow.memory
    def chat_history(self) -> ChatHistory:
        return self.chat_history
    
    @workflow.run
    async def run(self, input: ChatInteractionInputParams) -> ChatInteractionOutputParams:
        log.info("ChatInteraction started", input=input)
        
        chat_completion = await workflow.step(
            openai_chat_completion,
            OpenAIInputParams(
                user_content=input.user_content,
                system_content=input.system_content,
                base_url="https://ai.restack.io",
                model="restack-c1",
                messages=input.chat_history.messages if input.chat_history else []
            ),
            start_to_close_timeout=timedelta(seconds=120),
            retry_policy=RetryPolicy(
                maximum_attempts=1
            )
        )
        log.info("ChatInteraction completed", chat_completion=chat_completion)
        
        if input.chat_history:
            input.chat_history.messages.append((OpenAIInputParams(user_content=input.user_content, system_content=input.system_content), chat_completion))
        else:
            input.chat_history = ChatHistory(messages=[(OpenAIInputParams(user_content=input.user_content, system_content=input.system_content), chat_completion)])
        log.info("Messages updated", chat_history=input.chat_history)
        
        return ChatInteractionOutputParams(message=chat_completion.message)