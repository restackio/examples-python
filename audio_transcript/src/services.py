import asyncio
from src.client import client
from src.workflows.transcribe_translate import TranscribeTranslateWorkflow
from src.functions.transcribe_audio import transcribe_audio
from src.functions.translate_text import translate_text
from watchfiles import run_process
import webbrowser
import os

async def main():
    await asyncio.gather(
        client.start_service(
            workflows=[TranscribeTranslateWorkflow],
            functions=[transcribe_audio, translate_text]
        )
    )

def run_services():
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Service interrupted by user. Exiting gracefully.")

def watch_services():
    watch_path = os.getcwd()
    print(f"Watching {watch_path} and its subdirectories for changes...")
    webbrowser.open("http://localhost:5233")
    run_process(watch_path, recursive=True, target=run_services)

if __name__ == "__main__":
       run_services()
