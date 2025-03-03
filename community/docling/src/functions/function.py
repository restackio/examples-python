from restack_ai.function import function, log

@function.defn(name="welcome")
async def welcome(function_input: str) -> str:
    try:
        log.info("welcome function started", function_input=function_input)
        return f"Hello, {function_input}!"
    except Exception as e:
        log.error("welcome function failed", error=e)
        raise e
