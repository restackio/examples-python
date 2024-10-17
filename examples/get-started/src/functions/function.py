from restack_ai.function import function
from dataclasses import dataclass
@dataclass
class InputParams:
    name: str

@function.defn(name="goodbye")
async def goodbye(input: InputParams) -> str:
    return f"Goodbye, {input.name}!"

@function.defn(name="welcome")
async def welcome(input: InputParams) -> str:
    return f"Hello, {input.name}!"