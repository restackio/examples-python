from restack_ai.function import activity
from dataclasses import dataclass
@dataclass
class InputParams:
    name: str

@activity.defn(name="goodbye")
async def goodbye(input: InputParams) -> str:
    return f"Goodbye, {input.name}!"

@activity.defn(name="welcome")
async def welcome(input: InputParams) -> str:
    return f"Hello, {input.name}!"