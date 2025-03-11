from restack_ai.function import NonRetryableError, function, log


@function.defn(name="welcome")
async def welcome(function_input: str) -> str:
    try:
        log.info("welcome function started", function_input=function_input)
        return f"Hello, {function_input}!"
    except Exception as e:
        error_message = "Error during welcome function"
        log.error(error_message, error=e)
        raise NonRetryableError(message=error_message, error=e) from e
