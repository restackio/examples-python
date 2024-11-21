import asyncio
from src.client import client
from src.functions.transcribe import transcribe
from src.functions.translate import translate
from src.functions.fix_sentence import fix_sentence
from src.workflows.child import ChildWorkflow
from src.workflows.parent import ParentWorkflow

async def main():
    await asyncio.gather(
        client.start_service(
            workflows=[ParentWorkflow, ChildWorkflow],
            functions=[transcribe, translate, fix_sentence]
        )
    )

def run_services():
    asyncio.run(main())

if __name__ == "__main__":
    run_services()
