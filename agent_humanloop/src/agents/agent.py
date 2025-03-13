from dataclasses import dataclass
from datetime import timedelta

from restack_ai.agent import agent, import_functions, log

with import_functions():
    from src.functions.function import InputFeedback, goodbye
    from src.functions.function import (
        feedback as feedback_function,
    )

@dataclass
class Feedback:
    feedback: str

@dataclass
class End:
    end: bool

@agent.defn()
class AgentHumanLoop:
    def __init__(self) -> None:
        self.end_workflow = False
        self.feedbacks = []
    @agent.event
    async def event_feedback(self, feedback: Feedback) -> Feedback:
        result = await agent.step(function=feedback_function, function_input=InputFeedback(feedback.feedback), start_to_close_timeout=timedelta(seconds=120))
        log.info("Received feedback", result=result)
        return result

    @agent.event
    async def event_end(self, end: End) -> End:
        log.info("Received end", end=end)
        self.end_workflow = end.end
        return end

    @agent.run
    async def run(self):
        await agent.condition(
            lambda: self.end_workflow
        )
        result = await agent.step(function=goodbye, start_to_close_timeout=timedelta(seconds=120))
        log.info("Agent ended", result=result)
        return result


