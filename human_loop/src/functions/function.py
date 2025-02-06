from dataclasses import dataclass

from restack_ai.function import function, log


@dataclass
class InputFeedback:
    feedback: str


@function.defn()
async def goodbye() -> str:
    log.info("goodbye function started")
    return "Goodbye!"


@function.defn()
async def feedback(feedback_input: InputFeedback) -> str:
    log.info("feedback function started", input=feedback_input)
    return f"Received feedback: {feedback_input.feedback}"
