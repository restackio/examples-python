from restack_ai.function import function, log
from dataclasses import dataclass
import google.generativeai as genai

import os

@dataclass
class SummarizeTranscriptInput:
    transcript: str

@function.defn()
async def summarize_transcript(input: SummarizeTranscriptInput) -> str:
    try:
        log.info("summarize_transcript function started", input=input)
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = f"Please provide a concise summary of this meeting transcript: {input.transcript}"
        response = model.generate_content(prompt)
        log.info("summarize_transcript function completed", response=response.text)
        return response.text
    except Exception as e:
        log.error("summarize_transcript function failed", error=e)
        raise e
