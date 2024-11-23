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
        if not os.environ.get("GROQ_API_KEY"):
            raise Exception("GROQ_API_KEY is not set")
        
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


        filename, base64_content = input.file_data
        file_bytes = base64.b64decode(base64_content)
        transcription = client.audio.transcriptions.create(
            file=(filename, file_bytes), # Required audio file
            model="whisper-large-v3-turbo", # Required model to use for transcription
            # Best practice is to write the prompt in the language of the audio, use translate.google.com if needed
            prompt=f"Опиши о чем речь в аудио",  # Translation: Describe what the audio is about
            language="ru", # Original language of the audio
            response_format="json",  # Optional
            temperature=0.0  # Optional
        )

        log.info("transcribe function completed", transcription=transcription)
        return transcription
        

    except Exception as e:
        log.error("transcribe function failed", error=e)
        raise e
