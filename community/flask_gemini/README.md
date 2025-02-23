# Restack AI SDK - Flask + Gemini Generate Content Example

## Prerequisites

- Python 3.9 or higher
- Uv (for dependency management)
- Docker (for running the Restack services)
- Active [Google AI Studio](https://aistudio.google.com) account with API key

## Start Restack

To start the Restack, use the following Docker command:

```bash
docker run -d --pull always --name restack -p 5233:5233 -p 6233:6233 -p 7233:7233 -p 9233:9233 ghcr.io/restackio/restack:main
```

## Set `GEMINI_API_KEY` as an environment variable from [Google AI Studio](https://aistudio.google.com)

```bash
export GEMINI_API_KEY=<your-api-key>
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

## In a new terminal, run flask app:

If using uv:

```bash
uv run flask
```

If using pip:

```bash
python -c "from src.app import run_flask; run_flask()"
```

## Test your API with a POST request using curl:

```bash
curl -X POST \
  http://127.0.0.1:5000/api/schedule \
  -H "Content-Type: application/json" \
  -d '{"user_content": "Tell me a story"}'
```

This will schedule the `GeminiGenerateWorkflow` and print the result.

## Project Structure

- `src/`: Main source code directory
  - `client.py`: Initializes the Restack client
  - `functions/`: Contains function definitions
  - `workflows/`: Contains workflow definitions
  - `services.py`: Sets up and runs the Restack services
  - `app.py`: Flask app to schedule and run workflows
