from restack_ai.function import function, log, NonRetryableError

tries = 0

from pydantic import BaseModel

class ExampleFunctionInput(BaseModel):
    name: str

@function.defn()
async def example_function(input: ExampleFunctionInput) -> str:
    try:
        global tries

        if tries == 0:
            tries += 1
            raise NonRetryableError(message="Simulated failure")
      
        log.info("example function started", input=input)
        return f"Hello, {input.name}!"
    except Exception as e:
        log.error("example function failed", error=e)
        raise e
