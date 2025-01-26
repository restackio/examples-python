import asyncio
from src.functions.openai_chat import openai_chat
from src.client import client
from src.workflows.pdf import PdfWorkflow
from src.workflows.files import FilesWorkflow
from src.functions.google_doc_ai import google_doc_ai_pdf
from watchfiles import run_process
import webbrowser
import os

async def main():

    await asyncio.gather(
      await client.start_service(
          workflows= [PdfWorkflow, FilesWorkflow],
          functions= [google_doc_ai_pdf, openai_chat]
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