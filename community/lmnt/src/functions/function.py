from pydantic import BaseModel
from restack_ai.function import FunctionFailure, function, log

tries = 0


class ExampleFunctionInput(BaseModel):
    name: str

def raise_simulated_failure() -> None:
    error_message = "example function failed"
    log.error(error_message)
    raise FunctionFailure(error_message, non_retryable=False)


@function.defn()
async def example_function(example_function_input: ExampleFunctionInput) -> str:
    try:
        global tries # noqa: PLW0603

        if tries == 0:
            tries += 1
            raise_simulated_failure()

        log.info("example function started", input=example_function_input)
    except Exception as e:
        error_message = "example function failed"
        log.error(error_message, error=e)
        raise FunctionFailure(error_message, non_retryable=True) from e
    else:
        return f"Hello, {example_function_input.name}!"
