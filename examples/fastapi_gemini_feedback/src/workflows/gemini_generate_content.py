from restack_ai.workflow import workflow, workflow_import, log
from pydantic import BaseModel
from datetime import timedelta
from dataclasses import dataclass

@dataclass
class Feedback:
    feedback: str

@dataclass
class End:
    end: bool

with workflow_import():
    from src.functions.function import gemini_generate, FunctionInputParams
    from restack_google_gemini.task_queue import gemini_task_queue

class WorkflowInputParams(BaseModel):
    user_content: str

@workflow.defn(name="GeminiGenerateWorkflow")
class GeminiGenerateWorkflow:
    def __init__(self) -> None:
        self.end_workflow = False
        self.feedbacks = []
    @workflow.event
    async def event_feedback(self, feedback: Feedback) -> Feedback:
        log.info(f"Received feedback: {feedback.feedback}")
        return await workflow.step(gemini_generate, FunctionInputParams(user_content=f"{input.user_content}. Take into account all feedbacks: {feedback.feedback}"), start_to_close_timeout=timedelta(seconds=120))
    
    @workflow.event
    async def event_end(self, end: End) -> End:
        log.info(f"Received end: {end.end}")
        self.end_workflow = end.end
        return end
    @workflow.run
    async def run(self, input: WorkflowInputParams):
        await workflow.step(gemini_generate, FunctionInputParams(user_content=input.user_content), task_queue=gemini_task_queue, start_to_close_timeout=timedelta(seconds=120))
        await workflow.condition(
            lambda: self.end_workflow
        )
        return
