# Restack AI - Quickstart

This repository contains a quickstart for Restack.
It demonstrates how to set up a basic workflow and functions.

## Prerequisites

- Docker (for running Restack)
- Python 3.10 or higher

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

![Run workflows from UI](./screenshot-quickstart.png)

### from API

You can run workflows from the API by using the generated endpoint:

`POST http://localhost:6233/api/workflows/GreetingWorkflow`

### from any client

You can run workflows with any client connected to Restack, for example:

```bash
poetry run schedule
```

executes `schedule_workflow.py` which will connect to Restack and execute the `GreetingWorkflow` workflow.

## Deploy on Restack Cloud

To deploy the application on Restack, you can create an account at [https://console.restack.io](https://console.restack.io)
