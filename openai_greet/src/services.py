import asyncio
from src.functions.function import openai_greet
from src.client import client
from src.workflows.openai_greet import OpenaiGreetWorkflow
async def main():

    await client.start_service(
        workflows= [OpenaiGreetWorkflow],
        functions= [openai_greet],
    )

def run_services():
    asyncio.run(main())

if __name__ == "__main__":
    run_services()