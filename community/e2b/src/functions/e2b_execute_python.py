from e2b_code_interpreter import Sandbox
from restack_ai.function import function, log
from pydantic import BaseModel
from dotenv import load_dotenv
import json

load_dotenv()

class ExecutePythonInput(BaseModel):
    code: str = "print('hello world')"

@function.defn()
async def e2b_execute_python(input: ExecutePythonInput) -> str:
    try:
        # Create a new sandbox instance with a 60 second timeout
        sandbox = Sandbox(timeout=60)
        execution = sandbox.run_code(input.code)
        result = execution.text
        return result
    except Exception as e:
        log.error("e2b_execute_python function failed", error=e)
        raise e