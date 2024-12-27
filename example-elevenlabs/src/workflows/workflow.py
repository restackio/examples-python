from datetime import timedelta
from restack_ai.workflow import workflow, import_functions, log
import logging
from datetime import timedelta
from dotenv import load_dotenv
import os
# Load the environment variables
load_dotenv()

# Import the function
with import_functions():
    from src.functions.function import text_to_speech, isolate_audio


api_key = os.getenv("ELEVEN_LABS_API_KEY")

@workflow.defn()
class TextToSpeechWorkflow:
    @workflow.run
    async def run(self):
        log.info("TextToSpeechWorkflow started")

        # Define input parameters for the function
        input_data = {
            "text": "Hello, this is a test of the ElevenLabs text-to-speech converter using restack SDK.",
            "api_key": api_key,
            "voice_id": "JBFqnCBsd6RMkjVDRZzb",  # Optional, uses default if not provided
            "model_id": "eleven_monolingual_v1",  # Optional, uses default if not provided
            "twilio_encoding": False  # Optional, defaults to False
        }

        # Call the `text_to_speech` function as a workflow step
        result = await workflow.step(
            text_to_speech, 
            input=input_data, 
            start_to_close_timeout=timedelta(seconds=120)
        )

        # Save the audio file (optional)
        #try:
            #log.info("Saving audio file")
            #audio_data = base64.b64decode(result["media"]["payload"])
            #with open("output.mp3", "wb") as f:
               # f.write(audio_data)
           # log.info("Audio file saved successfully", file_path="output.mp3")
       # except Exception as e:
           # log.error("Failed to save the audio file", error=str(e))
           # raise e

        log.info("TextToSpeechWorkflow completed", result=result)
        return result
    
@workflow.defn()
class AudioIsolationWorkflow:
    @workflow.run
    async def run(self, input: dict):
        """
        Workflow to isolate audio from a given file path.

        :param input: A dictionary containing `api_key` and `audio_file_path`.
        """
        api_key = input.get("api_key")
        audio_file_path = input.get("audio_file_path")

        log.info("AudioIsolationWorkflow started")

        # Define input parameters for the `isolate_audio` function
        input_data = {
            "api_key": api_key,
            "audio_file_path": audio_file_path
        }

        # Call the `isolate_audio` function as a workflow step
        result = await workflow.step(
            isolate_audio,
            input=input_data,
            start_to_close_timeout=timedelta(seconds=120)
        )

        # Log the Base64-encoded audio payload
        log.info("Audio isolation completed successfully", base64_audio=result)

        # Return the Base64-encoded audio directly
        return result
