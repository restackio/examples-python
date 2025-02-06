from restack_ai.function import FunctionFailure, function, log


@function.defn()
async def welcome(welcome_input: str) -> str:
    try:
        log.info("welcome function started", input=welcome_input)
        result = f"Hello, {welcome_input}!"
    except Exception as e:
        error_message = "Failed to welcome"
        log.error(error_message, error=e)
        raise FunctionFailure(error_message, non_retryable=True) from e
    else:
        log.info("welcome function completed", result=result)
        return result
