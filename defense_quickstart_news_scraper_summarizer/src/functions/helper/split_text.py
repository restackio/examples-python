from restack_ai.function import function

@function.defn()
async def split_text(text: str, average_token_per_character: int = 3, max_tokens: int = 4096) -> list:
    chunks = []
    current_chunk = []
    current_length = 0

    for char in text:
        current_chunk.append(char)
        current_length += average_token_per_character

        if current_length >= max_tokens:
            chunks.append(''.join(current_chunk))
            current_chunk = []
            current_length = 0

    if current_chunk:
        chunks.append(''.join(current_chunk))

    return chunks