from restack_ai.function import function, log

@function.defn(name="welcome")
async def welcome(input: str) -> str:
    log.info("welcome function started", input=input)
    return f"Hello, {input}!"
