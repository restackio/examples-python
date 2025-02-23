# Restack AI SDK - Flask + TogetherAI with LlamaIndex Example

## Prerequisites

- Python 3.9 or higher
- Uv (for dependency management)
- Docker (for running the Restack services)
- Active [Together AI](https://together.ai) account with API key

## Start Restack

To start the Restack, use the following Docker command:

```bash
docker run -d --pull always --name restack -p 5233:5233 -p 6233:6233 -p 7233:7233 -p 9233:9233 ghcr.io/restackio/restack:main
```

## Set up your environment variables:

Copy `.env.example` to `.env` and add your Together AI API key:

```bash
cp .env.example .env
# Edit .env and add your TOGETHER_API_KEY
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

## In a new terminal, run flask app:

If using uv:

```bash
uv run flask
```

If using pip:

```bash
python -c "from src.app import run_flask; run_flask()"
```

## Test your Api a POST request using curl:

```bash
curl -X POST \
  http://localhost:5000/api/schedule \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Whats a cow?"}'
```

This will schedule the Llamaindex workflow with simple prompt and return the result.
