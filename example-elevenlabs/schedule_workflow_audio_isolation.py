import asyncio
import time
from restack_ai import Restack
from dotenv import load_dotenv
import os
# Load the environment variables
load_dotenv()
# Define the audio path and API key
audio_path = "/Users/sreedharpavushetty/Desktop/examples-python/example-elevenlabs/audio_files/suiii.mp3"  # Replace with your actual audio path
api_key = os.getenv("ELEVEN_LABS_API_KEY")


async def main(audio_path, api_key):
    # Initialize the Restack client
    client = Restack()

    # Generate a unique workflow ID
    workflow_id = f"{int(time.time() * 1000)}-AudioIsolationWorkflow"

    if not api_key:
        raise ValueError("API key not found. Set ELEVEN_LABS_API_KEY environment variable.")

    # Schedule the workflow with parameters
    run_id = await client.schedule_workflow(
        workflow_name="AudioIsolationWorkflow",
        workflow_id=workflow_id,
        input={
            "api_key": api_key,
            "audio_file_path": audio_path
        }
    )

    # Wait for the workflow result
    result = await client.get_workflow_result(
        workflow_id=workflow_id,
        run_id=run_id
    )

    # Log the result
    print(f"Workflow Result: {result}")


def run_schedule_workflow_audio_isolation():
    asyncio.run(main(audio_path, api_key))


if __name__ == "__main__":
    run_schedule_workflow_audio_isolation()
