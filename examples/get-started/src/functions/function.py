from restack_ai.function import function

@function.defn(name="welcome")
async def welcome(input: str) -> str:
    return f"Hello, {input}!"
