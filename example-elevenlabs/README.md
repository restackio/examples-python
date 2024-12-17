# Restack AI SDK - ElevenLabs Integration Example

This repository contains a simple example project to help you get started with the **Restack AI SDK** integrated with **ElevenLabs**. It demonstrates how to set up a basic workflow using the Restack SDK and ElevenLabs functions like **Text to Speech** and **Voice Isolation**.

## Prerequisites

* Python 3.8 or higher
* Poetry (for dependency management)
* Docker (for running the Restack services)

## Installation & Setup

### 1. Run Restack Local Engine with Docker

Start the Restack service using Docker:

```bash
docker run -d --pull always --name restack -p 5233:5233 -p 6233:6233 -p 7233:7233 ghcr.io/restackio/restack:main
```

### 2. Open the Web UI

After running the Restack service, open the web UI to see the workflows and monitor the execution:

```bash
http://localhost:5233
```

### 3. Clone This Repository

Clone the repository and navigate to the example folder:

```bash
git clone https://github.com/restackio/examples-python
cd examples-python/examples/elevenlabs
```

### 4. Install Dependencies Using Poetry

Set up the environment and install the necessary dependencies:

```bash
poetry env use 3.12
poetry shell
poetry install
poetry env info # Optional: copy the interpreter path to use in your IDE (e.g. Cursor, VSCode, etc.)
```

### 5. Run the Services

Start the Restack service with the defined workflows and functions:

```bash
poetry run dev
```

### 6. Export api key 

```bash
export ELEVEN_LABS_API_KEY= your_api_key_here
```


This will start the Restack service, enabling the functions for **Text to Speech** and **Voice Isolation**.

## Available Functions

The following two functions are defined in this setup:

* **text_to_speech**: Converts text input to spoken audio.
* **voice_isolation**: Isolates voice from background noise or other sounds.

## Example of Testing the Functions

### 1. Test Text to Speech

To test the **Text to Speech** function
First go to src/workflows/workflow.py and add your desired text in input_data and then use the following command:

```bash
poetry run text_to_speech
```

This will generate speech from the text and output the audio. 

### 2. Test Voice Isolation

To test the **Voice Isolation** function,
First go to **example-elevenlabs/schedule_workflow_audio_isolation.py** and add your audio file path in audio_path and then use the following command:

```bash
poetry run voice_isolation
```

This will isolate the voice from the provided audio file and output the isolated voice audio.

## Project Structure

* **src/**: Main source code directory
   * **client.py**: Initializes the Restack client.
   * **functions/**: Contains function definitions like `text_to_speech` and `voice_isolation`.
   * **workflows/**: Contains workflow definitions.
   * **services.py**: Sets up and runs the Restack services.
* **test_functions.py**: Example script to test the **Text to Speech** and **Voice Isolation** functions.
* **schedule_workflow.py**: Example script to schedule and run workflows if needed.
* **schedule_workflow.py**: Example script to schedule and run workflows if needed.
* **mpfile.mp3**: Example audio file

## Conclusion

This Example demonstrates how to integrate ElevenLabs functions with the Restack AI SDK. You can easily modify the workflows and functions to suit your specific needs, such as adding new AI capabilities or adjusting the parameters for text-to-speech and voice isolation tasks.
