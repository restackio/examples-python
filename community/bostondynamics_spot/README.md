# Restack AI SDK - Boston Dynamics Spot Example

This repository contains a simple example project to help you get started with the Restack AI SDK.

It demonstrates how to control Boston Dynamics Spot robot through a basic workflow and functions using the SDK.

## Prerequisites

- Python 3.8 or higher
- Uv (for dependency management)
- Docker (for running the Restack services)

## Usage

## Start Restack

To start the Restack, use the following Docker command:

```bash
docker run -d --pull always --name restack -p 5233:5233 -p 6233:6233 -p 7233:7233 -p 9233:9233 ghcr.io/restackio/restack:main
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
uv run services
```

If using pip:

```bash
pip install -e .
python -c "from src.services import run_services; run_services()"
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

If using uv:

```bash
uv run schedule
```

If using pip:

```bash
python -c "from schedule_workflow import run_schedule_workflow; run_schedule_workflow()"
```

executes `schedule_workflow.py` which will connect to Restack and execute the `TranscribeTranslateWorkflow` workflow.

## Project Structure

- `src/`: Main source code directory
  - `client.py`: Initializes the Restack client
  - `functions/`: Contains function definitions
  - `workflows/`: Contains workflow definitions
  - `services.py`: Sets up and runs the Restack services
- `schedule_workflow.py`: Example script to schedule and run a workflow
