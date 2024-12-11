import asyncio
from src.functions.ocr import ocr
from src.functions.another import another
from src.client import client
from src.workflows.pdf import PdfWorkflow
from src.workflows.files import FilesWorkflow
from restack_ai.restack import ServiceOptions

async def main():

    await asyncio.gather(
      await client.start_service(
          workflows= [PdfWorkflow, FilesWorkflow],
          functions= [another],
          options=ServiceOptions(
                max_concurrent_workflow_runs=1000
            )
      )
    )
    

def run_services():
    asyncio.run(main())

if __name__ == "__main__":
    run_services()