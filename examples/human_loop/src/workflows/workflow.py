from datetime import timedelta
from restack_ai.workflow import workflow, log
from src.functions.function import feedback as feedback_function, goodbye, InputFeedback
from dataclasses import dataclass

@dataclass
class Feedback:
    feedback: str

@dataclass
class End:
    end: bool

@workflow.defn(name="HumanLoopWorkflow")
class HumanLoopWorkflow:
    def __init__(self) -> None:
        self.end_workflow = False
        self.feedbacks = []
    @workflow.event
    async def event_feedback(self, feedback: Feedback) -> Feedback:
        log.info(f"Received feedback: {feedback.feedback}")
        return await workflow.step(feedback_function, InputFeedback(feedback.feedback), start_to_close_timeout=timedelta(seconds=120))
    
    @workflow.event
    async def event_end(self, end: End) -> End:
        log.info(f"Received end: {end.end}")
        self.end_workflow = end.end
        return end

    @workflow.run
    async def run(self):
        await workflow.condition(
            lambda: self.end_workflow
        )
        return await workflow.step(goodbye, start_to_close_timeout=timedelta(seconds=120))


