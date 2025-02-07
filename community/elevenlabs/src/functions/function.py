import base64

import aiofiles
import aiohttp
from restack_ai.function import FunctionFailure, function, log

HTTP_OK = 200

def raise_missing_api_key_error() -> None:
    error_message = "api_key is not set"
    log.error(error_message)
    raise FunctionFailure(error_message, non_retryable=True)

def raise_audio_isolation_failure() -> None:
    error_message = "Audio isolation failed"
    log.error(error_message)
    raise FunctionFailure(error_message, non_retryable=False)

def raise_audio_file_path_missing_error() -> None:
    error_message = "Audio file path is missing"
    log.error(error_message)
    raise ValueError(error_message)

def raise_text_is_empty_error() -> None:
    error_message = "Text is empty"
    log.error(error_message)
    raise ValueError(error_message)


@function.defn()
async def text_to_speech(text_to_speech_input: dict) -> dict:
    """Convert text to speech using ElevenLabs API.

    Args:
        text_to_speech_input (dict): A dictionary containing:
            - text (str): The text to convert to speech.
            - api_key (str): The ElevenLabs API key.
            - voice_id (str, optional): Voice ID to use.
            Defaults to "JBFqnCBsd6RMkjVDRZzb".
            - model_id (str, optional): Model ID to use.
            Defaults to "eleven_monolingual_v1".
            - twilio_encoding (bool, optional): If True,
            use Twilio-compatible output format.

    Returns:
        dict: A dictionary containing the base64-encoded audio payload.

    """
    try:
        # Log the start of the function
        log.info(
            "text_to_speech function started",
            text_to_speech_input=text_to_speech_input,
        )

        # Extract input parameters
        text = input.get("text", "")
        api_key = input.get("api_key")
        voice_id = input.get("voice_id", "JBFqnCBsd6RMkjVDRZzb")
        model_id = input.get("model_id", "eleven_monolingual_v1")
        twilio_encoding = input.get("twilio_encoding", False)

        # Validate input
        if not text:
            raise_text_is_empty_error()
        if not api_key:
            raise_missing_api_key_error()

        # Prepare request details
        base_url = "https://api.elevenlabs.io/v1"
        url = f"{base_url}/text-to-speech/{voice_id}"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": api_key,
        }
        data = {
            "text": text,
            "model_id": model_id,
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5,
            },
        }
        if twilio_encoding:
            data["output_format"] = "ulaw_8000"

        # Send the request
        async with aiohttp.ClientSession() as session, session.post(
            url,
            json=data,
            headers=headers,
            stream=True,
        ) as response:
            response.raise_for_status()

        # Collect response chunks and convert to base64
        content = b"".join(response.iter_content(chunk_size=1024))
        base64_audio = base64.b64encode(content).decode("utf-8")
    except Exception as e:
        error_message = "text_to_speech function failed"
        log.error(error_message, error=e)
        raise FunctionFailure(error_message) from e
    else:
        log.info("ElevenLabs conversion successful", audio_length=len(base64_audio))
        return {
            "media": {
                "payload": base64_audio,
            },
        }


@function.defn()
async def isolate_audio(isolate_audio_input: dict) -> dict:
    """Perform audio isolation.

    Uses the ElevenLabs API via direct
    HTTP POST request and returns Base64-encoded audio.

    Args:
        isolate_audio_input (dict): A dictionary containing:
            - api_key (str): The ElevenLabs API key.
            - audio_file_path (str): Path to the audio file to isolate.

    Returns:
        dict: A dictionary containing the Base64-encoded audio payload.

    """
    try:
        # Log the start of the function
        log.info(
            "isolate_audio function started",
            isolate_audio_input=isolate_audio_input,
        )

        # Extract input parameters
        api_key = isolate_audio_input.get("api_key")
        audio_file_path = isolate_audio_input.get("audio_file_path")

        # Validate input
        if not api_key:
            raise_missing_api_key_error()
        if not audio_file_path:
            raise_audio_file_path_missing_error()

        # Endpoint for ElevenLabs Audio Isolation
        url = "https://api.elevenlabs.io/v1/audio-isolation"

        # Read the audio file
        async with aiofiles.open(audio_file_path, "rb") as audio_file:
            # The `aiohttp` library automatically handles
            # the boundary for multipart requests
            files = {"audio": audio_file}
            headers = {
                "xi-api-key": api_key,  # Use the correct header key
            }

            # Make the POST request to the ElevenLabs API
            log.info("Sending request to ElevenLabs API...")
            async with aiohttp.ClientSession() as session, session.post(
                url, headers=headers, files=files,
            ) as response:
                response.raise_for_status()

        # Check response status
        if response.status_code != HTTP_OK:
            raise_audio_isolation_failure()

        # Extract the audio payload
        isolated_audio = response.content

        # Convert isolated audio to Base64
        base64_audio = base64.b64encode(isolated_audio).decode("utf-8")
    except Exception as e:
        error_message = "isolate_audio function failed"
        log.error(error_message, error=e)
        raise FunctionFailure(error_message) from e
    else:
        log.info(
            "isolate_audio function completed",
            base64_audio_length=len(base64_audio),
        )
        return {
            "media": {
                "payload": base64_audio,
            },
        }
