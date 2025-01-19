from restack_ai.function import function, FunctionFailure, log
from dataclasses import dataclass
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class TranscribeAudioInput:
    file_path: str

@function.defn()
async def transcribe_audio(input: TranscribeAudioInput):    
    if (os.environ.get("OPENAI_API_KEY") is None):
        raise FunctionFailure("OPENAI_API_KEY is not set", non_retryable=True)
    
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    try:
      response = client.audio.transcriptions.create(
          model="whisper-1",
          file=open(input.file_path, "rb")
      )
    except Exception as error:
      log.error("An error occurred during transcription", error)

    return response.text

