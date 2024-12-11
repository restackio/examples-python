import asyncio
from src.functions.ocr import ocr
from src.client import client
from src.workflows.workflow import PdfWorkflow
async def main():

    await client.start_service(
        workflows= [PdfWorkflow],
        functions= [ocr],
    )

def run_services():
    asyncio.run(main())

if __name__ == "__main__":
    run_services()