# Quickstart Llama Hackathon

[Everything you need for the Llama Impact Hackathon](https://docs.restack.io/community/hackathons/08-11-2024-llama-impact)

Restack AI - Streamlit + FastApi + TogetherAI with LlamaIndex Example

The AI workflow will search hacker news based on a query, crawl each project's website, and make summaries for the user.

## Prerequisites

- Python 3.12 or higher
- Uv (for dependency management)
- Docker (for running the Restack services)
- Active [Together AI](https://together.ai) account with API key

## YouTube walkthrough

[![Hackathon Walkthrough](https://img.youtube.com/vi/EgiYVXmnalU/0.jpg)](https://www.youtube.com/watch?v=EgiYVXmnalU)

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

## In a new terminal, run FastAPI app:

If using uv:

```bash
uv run app
```

If using pip:

```bash
python -c "from src.app import run_app; run_app()"
```

## In a new terminal, run the Streamlit frontend

If using uv:

```bash
uv run streamlit run frontend.py
```

If using pip:

```bash
python -c "from src.frontend import run_frontend; run_frontend()"
```

## You can test the API endpoint without the Streamlit UI with:

```bash
curl -X POST \
  http://localhost:8000/api/schedule \
  -H "Content-Type: application/json" \
  -d '{"query": "AI", "count": 5}'
```

This will schedule the workflow and return the result.
