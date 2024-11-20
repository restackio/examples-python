from restack_ai.function import function, log
from dataclasses import dataclass
from groq import Groq
import os
import base64
@dataclass
class FunctionInputParams:
    file_data: tuple[str, str]

@function.defn()
async def transcribe(input: FunctionInputParams):
    try:
        log.info("transcribe function started", input=input)
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

        filename, base64_content = input.file_data
        file_bytes = base64.b64decode(base64_content)
        transcription = client.audio.transcriptions.create(
            file=(filename, file_bytes), # Required audio file
            model="whisper-large-v3-turbo", # Required model to use for transcription
            prompt="Specify context or spelling",  # Optional
            response_format="json",  # Optional
            language="ru",
            temperature=0.0  # Optional
        )

        log.info("transcribe function completed", transcription=transcription)
        return transcription.text
        

    except Exception as e:
        log.error("transcribe function failed", error=e)
        raise e
