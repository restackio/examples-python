from datetime import timedelta
from restack_ai.workflow import workflow, import_functions, log
from dataclasses import dataclass

with import_functions():
    from src.functions.function import feedback as feedback_function, goodbye, InputFeedback

@dataclass
class Feedback:
    feedback: str

@dataclass
class End:
    end: bool

@workflow.defn()
class HumanLoopWorkflow:
    def __init__(self) -> None:
        self.end_workflow = False
        self.feedbacks = []
    @workflow.event
    async def event_feedback(self, feedback: Feedback) -> Feedback:
        result = await workflow.step(feedback_function, InputFeedback(feedback.feedback), start_to_close_timeout=timedelta(seconds=120))
        log.info("Received feedback", result=result)
        return result
    
    @workflow.event
    async def event_end(self, end: End) -> End:
        log.info("Received end", end=end)
        self.end_workflow = end.end
        return end

    @workflow.run
    async def run(self):
        await workflow.condition(
            lambda: self.end_workflow
        )
        result = await workflow.step(goodbye, start_to_close_timeout=timedelta(seconds=120))
        log.info("Workflow ended", result=result)
        return result


