# Restack AI SDK with Weaviate - Get Started Example

This repository contains a simple example project to help you get started with the Restack AI SDK and Weaviate. It demonstrates how to set up a basic workflow and functions using the Restack AI SDK to interact with a Weaviate vector database.

The example is a follow along of <https://weaviate.io/developers/weaviate/starter-guides/custom-vectors> and includes:

- Setting up a Weaviate client
- Seeding a Weaviate database with Jeopardy questions
- Performing vector searches using Restack AI functions

## Prerequisites

- Python 3.9 or higher
- Uv (for dependency management)

## Environment Variables

To use this project, you need to have access to Weaviate Cloud. Follow these steps to obtain your `WEAVIATE_URL` and `WEAVIATE_API_KEY`:

1. **Sign up for Weaviate Cloud**: If you haven't already, create an account on [Weaviate Cloud](https://console.weaviate.cloud).
2. **Create a Weaviate Instance**: Once logged in, create a new Weaviate instance.
3. **Retrieve Credentials**: After your instance is set up, navigate to the instance details page to find your `WEAVIATE_URL` and `WEAVIATE_API_KEY`.

Add these credentials to your `.env` file.

## Usage

### Start Restack Engine

Using `docker run`:

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

### Scheduling Workflows

To schedule and run the example workflows, use:

If using uv:

```bash
uv run schedule-seed-workflow
```

If using pip:

```bash
python -c "from src.schedule_workflow import run_schedule_seed_workflow; run_schedule_seed_workflow()"
```

This will schedule the "SeedWorkflow" and print the result.

To run the search workflow, use:

If using uv:

```bash
uv run schedule-search-workflow
```

If using pip:

```bash
python -c "from src.schedule_workflow import run_schedule_search_workflow; run_schedule_search_workflow()"
```

This will schedule the "SearchWorkflow" and print the result.
