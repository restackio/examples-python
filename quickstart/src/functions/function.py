from pydantic import BaseModel
from restack_ai.function import FunctionFailure, function, log


class WelcomeInput(BaseModel):
    name: str


@function.defn()
async def welcome(welcome_input: WelcomeInput) -> str:
    try:
        log.info("welcome function started", input=welcome_input)
        message = f"Hello, {welcome_input.name}!"
    except Exception as e:
        error_message = "welcome function failed"
        log.error(error_message, error=e)
        raise FunctionFailure(error_message, non_retryable=True) from e
    else:
        return message
