from restack_ai.workflow import workflow, import_functions, log
from pydantic import BaseModel
from datetime import timedelta
from dataclasses import dataclass

with import_functions():
    from src.functions.function import gemini_generate, FunctionInputParams

@dataclass
class Feedback:
    feedback: str

@dataclass
class End:
    end: bool

class WorkflowInputParams(BaseModel):
    user_content: str

@workflow.defn()
class GeminiGenerateWorkflow:
    def __init__(self) -> None:
        self.end_workflow = False
        self.feedbacks = []
        self.user_content = ""
    @workflow.event
    async def event_feedback(self, feedback: Feedback) -> Feedback:
        log.info(f"Received feedback: {feedback.feedback}")
        self.feedbacks.append(feedback.feedback)
        return await workflow.step(gemini_generate, FunctionInputParams(user_content=f"{self.user_content}. Take into account all feedbacks: {self.feedbacks}"), start_to_close_timeout=timedelta(seconds=120))
    
    @workflow.event
    async def event_end(self, end: End) -> End:
        log.info(f"Received end")
        self.end_workflow = True
        return end
    @workflow.run
    async def run(self, input: WorkflowInputParams):
        self.user_content = input.user_content
        await workflow.step(gemini_generate, FunctionInputParams(user_content=input.user_content), start_to_close_timeout=timedelta(seconds=120))
        await workflow.condition(
            lambda: self.end_workflow
        )
        return
