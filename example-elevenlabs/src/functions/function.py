from restack_ai.function import function, log
import requests
import base64
import json
import logging


@function.defn()
async def text_to_speech(input: dict) -> dict:
    """
    Convert text to speech using ElevenLabs API.
    Args:
        input (dict): A dictionary containing:
            - text (str): The text to convert to speech.
            - api_key (str): The ElevenLabs API key.
            - voice_id (str, optional): Voice ID to use. Defaults to "JBFqnCBsd6RMkjVDRZzb".
            - model_id (str, optional): Model ID to use. Defaults to "eleven_monolingual_v1".
            - twilio_encoding (bool, optional): If True, use Twilio-compatible output format.
    Returns:
        dict: A dictionary containing the base64-encoded audio payload.
    """
    try:
        # Log the start of the function
        log.info("text_to_speech function started", input=input)

        # Extract input parameters
        text = input.get("text", "")
        api_key = input.get("api_key")
        voice_id = input.get("voice_id", "JBFqnCBsd6RMkjVDRZzb")
        model_id = input.get("model_id", "eleven_monolingual_v1")
        twilio_encoding = input.get("twilio_encoding", False)

        # Validate input
        if not text:
            raise ValueError("Text is empty.")
        if not api_key:
            raise ValueError("API key is missing.")

        # Prepare request details
        base_url = "https://api.elevenlabs.io/v1"
        url = f"{base_url}/text-to-speech/{voice_id}"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": api_key
        }
        data = {
            "text": text,
            "model_id": model_id,
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }
        if twilio_encoding:
            data["output_format"] = "ulaw_8000"

        # Send the request
        response = requests.post(url, json=data, headers=headers, stream=True)
        response.raise_for_status()

        # Collect response chunks and convert to base64
        content = b''.join(response.iter_content(chunk_size=1024))
        base64_audio = base64.b64encode(content).decode('utf-8')

        log.info("ElevenLabs conversion successful", audio_length=len(base64_audio))
        return {
            "media": {
                "payload": base64_audio
            }
        }
    except Exception as e:
        log.error("text_to_speech function failed", error=str(e))
        raise e

# Initialize logger
#log = logging.getLogger(__name__)

@function.defn()
async def isolate_audio(input: dict) -> dict:
    """
    Perform audio isolation using the ElevenLabs API via direct HTTP POST request and return Base64-encoded audio.
    Args:
        input (dict): A dictionary containing:
            - api_key (str): The ElevenLabs API key.
            - audio_file_path (str): Path to the audio file to isolate.
    Returns:
        dict: A dictionary containing the Base64-encoded audio payload.
    """
    try:
        # Log the start of the function
        log.info("isolate_audio function started", input=input)

        # Extract input parameters
        api_key = input.get("api_key")
        audio_file_path = input.get("audio_file_path")

        # Validate input
        if not api_key:
            raise ValueError("API key is missing.")
        if not audio_file_path:
            raise ValueError("Audio file path is missing.")

        # Endpoint for ElevenLabs Audio Isolation
        url = "https://api.elevenlabs.io/v1/audio-isolation"

        # Read the audio file
        with open(audio_file_path, "rb") as audio_file:
            # The `requests` library automatically handles the boundary for multipart requests
            files = {"audio": audio_file}
            headers = {
                "xi-api-key": api_key  # Use the correct header key
            }

            # Make the POST request to the ElevenLabs API
            log.info("Sending request to ElevenLabs API...")
            response = requests.post(url, headers=headers, files=files)

        # Check response status
        if response.status_code != 200:
            log.error("Audio isolation failed", status_code=response.status_code, response=response.text)
            raise ValueError(f"API request failed with status code {response.status_code}: {response.text}")

        # Extract the audio payload
        isolated_audio = response.content

        # Convert isolated audio to Base64
        base64_audio = base64.b64encode(isolated_audio).decode("utf-8")

        log.info("Audio isolation successful", base64_audio_length=len(base64_audio))
        return {
            "media": {
                "payload": base64_audio
            }
        }
    except Exception as e:
        log.error("isolate_audio function failed", error=str(e))
        raise e
