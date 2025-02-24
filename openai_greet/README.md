# Restack AI SDK - OpenAI Greet Example

## Prerequisites

- Python 3.8 or higher
- Uv (for dependency management)
- Docker (for running the Restack services)
- Active [OpenAI](https://platform.openai.com) account with API key

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
uv run dev
```

If using pip:

```bash
pip install -e .
python -c "from src.services import watch_services; watch_services()"
```

## Run workflows

### from UI

You can run workflows from the UI by clicking the "Run" button.

![Run workflows from UI](./screenshot-quickstart.png)

### from API

You can run workflows from the API by using the generated endpoint:

`POST http://localhost:6233/api/workflows/OpenaiGreetWorkflow`

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

executes `schedule_workflow.py` which will connect to Restack and execute the `OpenaiGreetWorkflow` workflow.

## Deploy on Restack Cloud

To deploy the application on Restack, you can create an account at [https://console.restack.io](https://console.restack.io)
