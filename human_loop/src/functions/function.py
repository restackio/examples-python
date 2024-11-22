from restack_ai.function import function, log
from dataclasses import dataclass
@dataclass
class InputFeedback:
    feedback: str

@function.defn()
async def goodbye() -> str:
    log.info("goodbye function started")
    return f"Goodbye!"

@function.defn()
async def feedback(input: InputFeedback) -> str:
    log.info("feedback function started", input=input)
    return f"Received feedback: {input.feedback}"
