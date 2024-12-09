import asyncio
from src.client import client
from src.workflows.transcribe_translate import TranscribeTranslateWorkflow
from src.functions.transcribe_audio import transcribe_audio
from src.functions.translate_text import translate_text

async def main():
    await asyncio.gather(
        client.start_service(
            workflows=[TranscribeTranslateWorkflow],
            functions=[transcribe_audio, translate_text]
        )
    )

def run_services():
    asyncio.run(main())

if __name__ == "__main__":
    run_services()
