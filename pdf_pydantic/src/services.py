import asyncio
from src.functions.torch_ocr import torch_ocr
from src.functions.openai_chat import openai_chat
from src.client import client
from src.workflows.pdf import PdfWorkflow
from src.workflows.files import FilesWorkflow

async def main():

    await asyncio.gather(
      await client.start_service(
          workflows= [PdfWorkflow, FilesWorkflow],
          functions= [torch_ocr, openai_chat]
      )
    )
    
def run_services():
    asyncio.run(main())

if __name__ == "__main__":
    run_services()