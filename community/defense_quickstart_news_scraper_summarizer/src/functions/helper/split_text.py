from restack_ai.function import function

from pydantic import BaseModel

class SplitTextInput(BaseModel):
    text: str
    average_token_per_character: int = 3
    max_tokens: int = 4096

@function.defn()
async def split_text(input: SplitTextInput) -> list:
    chunks = []
    current_chunk = []
    current_length = 0

    for char in input.text:
        current_chunk.append(char)
        current_length += input.average_token_per_character

        if current_length >= input.max_tokens:
            chunks.append(''.join(current_chunk))
            current_chunk = []
            current_length = 0

    if current_chunk:
        chunks.append(''.join(current_chunk))

    return chunks