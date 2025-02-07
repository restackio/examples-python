import asyncio
import logging
import os
import time

from dotenv import load_dotenv
from restack_ai import Restack

# Load the environment variables
load_dotenv()
# Define the audio path and API key
audio_path = """
/Users/sreedharpavushetty/Desktop/examples-python/example-elevenlabs/audio_files/suiii.mp3
"""  # Replace with your actual audio path
api_key = os.getenv("ELEVEN_LABS_API_KEY")


async def main(audio_path: str, api_key: str) -> None:
    # Initialize the Restack client
    client = Restack()

    # Generate a unique workflow ID
    workflow_id = f"{int(time.time() * 1000)}-AudioIsolationWorkflow"

    if not api_key:
        error_message = """
        API key not found.
        Set ELEVEN_LABS_API_KEY environment variable.
        """
        logging.error(error_message)
        raise ValueError(error_message)

    # Schedule the workflow with parameters
    run_id = await client.schedule_workflow(
        workflow_name="AudioIsolationWorkflow",
        workflow_id=workflow_id,
        input={
            "api_key": api_key,
            "audio_file_path": audio_path,
        },
    )

    # Wait for the workflow result
    result = await client.get_workflow_result(
        workflow_id=workflow_id,
        run_id=run_id,
    )

    # Log the result
    logging.info("Workflow Result: %s", result)


def run_schedule_workflow_audio_isolation() -> None:
    asyncio.run(main(audio_path=audio_path, api_key=api_key))


if __name__ == "__main__":
    run_schedule_workflow_audio_isolation()
