# Restack AI - Email Sender example

This example showcases how to send emails with a Restack workflow using the sendgrid api. You can easily choose another email provider and update the code.
You can schedule two scenarios of the workflow.

1. It will be successfull and send an email.
2. The email content generation step will fail once to showcase how Restack handles retries automatically. Once failure is caught, step will be retry automatically and rest of workflow will be executed as expected and email will be sent.

## Prerequisites

- Python 3.10 or higher
- Uv (for dependency management)
- Docker (for running the Restack services)

## Start Restack

To start the Restack, use the following Docker command:

```bash
docker run -d --pull always --name restack -p 5233:5233 -p 6233:6233 -p 7233:7233 -p 9233:9233 ghcr.io/restackio/restack:main
```

## Environment variables

Create .env file with: STRIPE_SECRET_KEY and OPENAI_API_KEY

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

## Run the services:

If using uv:

```bash
uv run services
```

If using pip:

```bash
python -c "from src.services import run_services; run_services()"
```

## In a new terminal, schedule the workflow:

If using uv:

```bash
uv run schedule
```

If using pip:

```bash
python -c "from schedule_workflow import run_schedule_workflow; run_schedule_workflow()"
```

This will schedule the `SendEmailWorkflow` and print the result.

### To simulate a flow where the step for sending email fails and the retry is automatically handled by Restack AI use run:

If using uv:

```bash
uv run schedule_failure
```

If using pip:

```bash
python -c "from schedule_workflow_failure import run_schedule_workflow_failure; run_schedule_workflow_failure()"
```
