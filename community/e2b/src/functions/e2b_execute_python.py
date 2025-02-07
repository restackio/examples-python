from dotenv import load_dotenv
from e2b_code_interpreter import Sandbox
from pydantic import BaseModel
from restack_ai.function import FunctionFailure, function, log

load_dotenv()


class ExecutePythonInput(BaseModel):
    code: str = "print('hello world')"


@function.defn()
async def e2b_execute_python(e2b_execute_python_input: ExecutePythonInput) -> str:
    try:
        # Create a new sandbox instance with a 60 second timeout
        sandbox = Sandbox(timeout=60)
        execution = sandbox.run_code(e2b_execute_python_input.code)
    except Exception as e:
        error_message = "e2b_execute_python function failed"
        log.error(error_message, error=e)
        raise FunctionFailure(error_message, non_retryable=True) from e
    else:
        log.info("e2b_execute_python function succeeded")
        return execution.text
