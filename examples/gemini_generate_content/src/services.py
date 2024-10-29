import asyncio
from src.client import client
from src.functions.function import gemini_generate_opposite
from src.workflows.gemini_generate_content import GeminiGenerateOppositeWorkflow

async def main():
    await client.start_service({
        "workflows": [GeminiGenerateOppositeWorkflow],
        "functions": [gemini_generate_opposite]
    })

def run_services():
    asyncio.run(main())

if __name__ == "__main__":
    run_services()