from restack_ai.function import function
from dataclasses import dataclass
@dataclass
class InputFeedback:
    feedback: str

@function.defn()
async def goodbye() -> str:
    return f"Goodbye!"

@function.defn(name="feedback")
async def feedback(input: InputFeedback) -> str:
    return f"Received feedback: {input.feedback}"