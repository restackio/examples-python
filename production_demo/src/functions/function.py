from restack_ai.function import function, log, FunctionFailure

tries = 0

@function.defn()
async def example_function(input: str) -> str:
    try:
        global tries

        if tries == 0:
            tries += 1
            raise FunctionFailure(message="Simulated failure", non_retryable=False)
      
        log.info("example function started", input=input)
        return f"Hello, {input}!"
    except Exception as e:
        log.error("example function failed", error=e)
        raise e
