# Restack AI - Audio translation example

This example showcases how to transcribe an mp3 audio and then translate the generated text to a target language, all done in a single workflow defined with Restack AI.

## Prerequisites

- Docker (for running Restack)
- Python 3.10 or higher
- Poetry (for dependency management)

## Start Restack

To start the Restack, use the following Docker command:

```bash
docker run -d --pull always --name restack -p 5233:5233 -p 6233:6233 -p 7233:7233 ghcr.io/restackio/restack:main
```

## Start python shell

```bash
poetry env use 3.10 && poetry shell
```

## Install dependencies

```bash
poetry install
```

```bash
poetry env info # Optional: copy the interpreter path to use in your IDE (e.g. Cursor, VSCode, etc.)
```

```bash
poetry run dev
```

## Run workflows

### from UI

You can run workflows from the UI by clicking the "Run" button.

![Run workflows from UI](./ui-screenshot.png)

### from API

You can run workflows from the API by using the generated endpoint:

`POST http://localhost:6233/api/workflows/TranscribeTranslateWorkflow`

### from any client

You can run workflows with any client connected to Restack, for example:

```bash
poetry run schedule
```

executes `schedule_workflow.py` which will connect to Restack and execute the `TranscribeTranslateWorkflow` workflow.

## Deploy on Restack Cloud

To deploy the application on Restack, you can create an account at [https://console.restack.io](https://console.restack.io)
