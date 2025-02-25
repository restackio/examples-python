# Restack AI SDK - ElevenLabs Integration Example

This repository contains a simple example project to help you get started with the **Restack AI SDK** integrated with **ElevenLabs**. It demonstrates how to set up a basic workflow using the Restack SDK and ElevenLabs functions like **Text to Speech** and **Voice Isolation**.

## Prerequisites

- Python 3.8 or higher
- Uv (for dependency management)
- Docker (for running the Restack services)

## Installation & Setup

## Run Restack Local Engine with Docker

Start the Restack service using Docker:

```bash
docker run -d --pull always --name restack -p 5233:5233 -p 6233:6233 -p 7233:7233 -p 9233:9233 ghcr.io/restackio/restack:main
```

## Open the Web UI

After running the Restack service, open the web UI to see the workflows and monitor the execution:

```bash
http://localhost:5233
```

## Clone This Repository

Clone the repository and navigate to the example folder:

```bash
git clone https://github.com/restackio/examples-python
cd examples-python/examples/elevenlabs
```

## Start python shell

If using uv:

```bash
uv venv && source .venv/bin/activate
```

If using pip:

```bash
python -m venv .venv && source .venv/bin/activate
```

## Install dependencies

If using uv:

```bash
uv sync
uv run dev
```

If using pip:

```bash
pip install -e .
python -c "from src.services import watch_services; watch_services()"
```

## Export api key

```bash
export ELEVEN_LABS_API_KEY= your_api_key_here
```

This will start the Restack service, enabling the functions for **Text to Speech** and **Voice Isolation**.

## Available Functions

The following two functions are defined in this setup:

- **text_to_speech**: Converts text input to spoken audio.
- **voice_isolation**: Isolates voice from background noise or other sounds.

## Example of Testing the Functions

### 1. Test Text to Speech

To test the **Text to Speech** function
First go to src/workflows/workflow.py and add your desired text in input_data and then use the following command:

If using uv:

```bash
uv run text_to_speech
```

If using pip:

```bash
python -c "from src.schedule_workflow import run_schedule_workflow; run_schedule_workflow()"
```

This will generate speech from the text and output the audio.

## Test Voice Isolation

To test the **Voice Isolation** function,
First go to **example-elevenlabs/schedule_workflow_audio_isolation.py** and add your audio file path in audio_path and then use the following command:

If using uv:

```bash
uv run voice_isolation
```

If using pip:

```bash
python -c "from src.schedule_workflow_audio_isolation import run_schedule_workflow_audio_isolation; run_schedule_workflow_audio_isolation()"
```

This will isolate the voice from the provided audio file and output the isolated voice audio.

## Project Structure

- **src/**: Main source code directory
  - **client.py**: Initializes the Restack client.
  - **functions/**: Contains function definitions like `text_to_speech` and `voice_isolation`.
  - **workflows/**: Contains workflow definitions.
  - **services.py**: Sets up and runs the Restack services.
- **test_functions.py**: Example script to test the **Text to Speech** and **Voice Isolation** functions.
- **schedule_workflow.py**: Example script to schedule and run workflows if needed.
- **schedule_workflow.py**: Example script to schedule and run workflows if needed.
- **mpfile.mp3**: Example audio file

## Conclusion

This Example demonstrates how to integrate ElevenLabs functions with the Restack AI SDK. You can easily modify the workflows and functions to suit your specific needs, such as adding new AI capabilities or adjusting the parameters for text-to-speech and voice isolation tasks.
