from restack_ai.workflow import workflow, import_functions, log, RetryPolicy
from datetime import timedelta
from pydantic import BaseModel

with import_functions():
    from src.functions.openai_chat_completion import openai_chat_completion, OpenAIInputParams, OpenAIOutputParams
    from .chat_interaction import ChatInteraction, ChatInteractionInputParams, ChatInteractionOutputParams
    from src.functions.get_workflow_memory import get_workflow_memory, GetWorkflowMemoryInput

class ChatSessionInputParams(BaseModel):
    chat_id: str = "Add your name as chat_id"
    user_content: str = "What is restack?"
    system_content: str = "You are a helpful assistant."

class ChatSessionOutputParams(BaseModel):
    message: str

@workflow.defn()
class ChatSession:
    @workflow.run
    async def run(self, input: ChatSessionInputParams) -> ChatSessionOutputParams:
        log.info("ChatSession started", input=input)
        
        interaction_workflow_id = f"local-chat-interaction-{input.chat_id}"
        interaction_input = ChatInteractionInputParams(
            chat_id=input.chat_id,
            user_content=input.user_content,
            system_content=input.system_content,
            chat_history=None
        )
        
        # Attempt to retrieve chat history using get_workflow_memory
        memory_input = GetWorkflowMemoryInput(
            workflow_id=interaction_workflow_id,
            memory_name="chat_history"
        )
        try:
            chat_history = await workflow.step(get_workflow_memory, memory_input, retry_policy=RetryPolicy(maximum_attempts=1))
            interaction_input.chat_history = chat_history
            log.info("Existing chat history retrieved", chat_history=chat_history)
        except Exception as e:
            log.error("No existing chat history found, starting new session", error=str(e))
            interaction_input.chat_history = None  # Ensure no history is passed if retrieval fails
        
        # Using execute_child to start and wait for the child workflow result
        result = await workflow.child_execute(
            ChatInteraction,
            workflow_id=interaction_workflow_id,
            input=interaction_input
        )
        
        log.info("ChatSession completed", result=result)
        
        return ChatSessionOutputParams(message=result.message)