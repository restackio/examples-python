import asyncio
from src.client import client
from src.functions.function import gemini_generate
from src.workflows.gemini_generate_content import GeminiGenerateWorkflow
async def main():
    await client.start_service(
        workflows= [GeminiGenerateWorkflow],
        functions= [gemini_generate]
    )

def run_services():
    asyncio.run(main())

if __name__ == "__main__":
    run_services()