from restack_ai.function import function, log

@function.defn()
async def welcome(input: str) -> str:
    try:
        log.info("welcome function started", input=input)
        return f"Hello, {input}!"
    except Exception as e:
        log.error("welcome function failed", error=e)
        raise e
