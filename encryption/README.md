# Restack AI - Encryption Example

This repository contains a simple example project to help you get started with the Restack AI SDK. It demonstrates how to set up a basic workflow and functions using the SDK.

## Prerequisites

- Python 3.8 or higher
- Uv (for dependency management)
- Docker (for running the Restack services)

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

## In a new terminal, run the encryption codec server:

If using uv:

```bash
uv run codec
```

If using pip:

```bash
python -c "from src.codec_server import run_codec_server; run_codec_server()"
```

### In an another terminal, run the workflow

If using uv:

```bash
uv run schedule
```

If using pip:

```bash
python -c "from src.schedule_workflow import run_schedule_workflow; run_schedule_workflow()"
```

### To decrypt use http://localhost:8081 in the UI settings as the codec address

## Project Structure

- `src/`: Main source code directory
  - `client.py`: Initializes the Restack client
  - `functions/`: Contains function definitions
  - `workflows/`: Contains workflow definitions
  - `services.py`: Sets up and runs the Restack services
- `schedule_workflow.py`: Example script to schedule and run a workflow
