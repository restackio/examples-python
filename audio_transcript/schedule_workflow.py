import asyncio
import time
from restack_ai import Restack
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

@dataclass
class InputParams:
    file_path: str
    target_language: str

async def main(input: InputParams):
    client = Restack()

    workflow_id = f"{int(time.time() * 1000)}-TranscribeTranslateWorkflow"

    run_id = await client.schedule_workflow(
        workflow_name="TranscribeTranslateWorkflow",
        workflow_id=workflow_id,
        input={
            "file_path": input.file_path,
            "target_language": input.target_language
        }
    )

    await client.get_workflow_result(
        workflow_id=workflow_id,
        run_id=run_id
    )

    exit(0)

def run_schedule_workflow():
    asyncio.run(main(InputParams(file_path="./test.mp3", target_language="Spanish")))

if __name__ == "__main__":
    run_schedule_workflow()
