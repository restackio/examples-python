from pydantic import BaseModel
from restack_ai.function import function, log

class FunctionInput(BaseModel):
    file_type: str
    file_binary:str

@function.defn(name="another")
async def another(input: FunctionInput) -> str:
    try:
        return input.file_type
    except Exception as e:
        log.error(f"Error in ocr function: {e}")
        raise e
