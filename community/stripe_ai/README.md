# Restack AI - Stripe Ai example

This repository contains a an example on how restack can use langchain and the stripe ai sdk to create a product with a price and also create a payment link for it.

## Prerequisites

- Python 3.10 or higher
- Uv (for dependency management)
- Docker (for running the Restack services)

## Start Restack

To start the Restack, use the following Docker command:

```bash
docker run -d --pull always --name restack -p 5233:5233 -p 6233:6233 -p 7233:7233 -p 9233:9233 ghcr.io/restackio/restack:main
```

## Create .env file with: STRIPE_SECRET_KEY, LANGCHAIN_API_KEY and OPENAI_API_KEY

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

## In a new terminal, schedule the workflow:

If using uv:

```bash
uv run schedule
```

If using pip:

```bash
python -c "from schedule_workflow import run_schedule_workflow; run_schedule_workflow()"
```

This will schedule the `CreatePaymentLinkWorkflow` and print the result.
