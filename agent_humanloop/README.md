# Restack AI - Agent with human in the loop

This repository contains an example Agent with human in the loop with Restack.
It demonstrates how to set up a basic Agent and functions.

## Prerequisites

- Docker (for running Restack)
- Python 3.10 or higher

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

## Run agents

### from UI

You can run agents from the UI by clicking the "Run" button.

![Run agents from UI](./screenshot-quickstart.png)

### from API

You can run agents from the API by using the generated endpoint:

`POST http://localhost:6233/api/agents/AgentHumanLoop`

### from any client

You can run agents with any client connected to Restack, for example:

If using uv:

```bash
uv run schedule
```

If using pip:

```bash
python -c "from schedule_agent import run_schedule_agent; run_schedule_agent()"
```

executes `schedule_agent.py` which will connect to Restack and execute the `AgentHumanLoop` agent.

## Deploy on Restack Cloud

To deploy the application on Restack, you can create an account at [https://console.restack.io](https://console.restack.io)
