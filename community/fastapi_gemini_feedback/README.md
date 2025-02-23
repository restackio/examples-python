# Restack AI SDK - FastAPI + Gemini Generate Content Example

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

## Configure your Gemini API key using one of these methods:

a. Set as environment variable:

```bash
export GEMINI_API_KEY=<your-api-key>
```

b. Create a `.env` file:

- Copy `.env.example` to `.env` in the `fastapi_gemini_feedback` folder
- Add your API key from [Google AI Studio](https://aistudio.google.com):

```bash
GEMINI_API_KEY=<your-api-key>
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
uv run app
```

If using pip:

```bash
python -c "from src.app import run_app; run_app()"
```

The app will run at http://0.0.0.0:5001

## POST to `http://0.0.0.0:5000/api/schedule` with the following JSON body:

```json
{
  "user_content": "Tell me a story"
}
```

Or using curl in a new terminal:

```bash
curl -X POST http://0.0.0.0:5001/api/schedule -H "Content-Type: application/json" -d '{"user_content": "Tell me a story"}'
```

This will schedule the `GeminiGenerateWorkflow` and print the result. The workflow will continue running, waiting for feedback.

## POST to `http://0.0.0.0:5000/api/event/feedback` with the following JSON body:

```json
{
  "feedback": "The story is too long",
  "workflow_id":"<workflow_id>",
  "run_id":"<run_id>""
}
```

Or using curl:

```bash
curl -X POST http://0.0.0.0:5001/api/event/feedback -H "Content-Type: application/json" -d '{"feedback": "The story is too long", "workflow_id": "<workflow_id>", "run_id": "<run_id>"}'
```

Use the `workflow_id` and `run_id` returned from the previous schedule API call to send feedback to the workflow.

## POST to `http://0.0.0.0:5001/api/event/end` to end the workflow with the following JSON body:

```json
{
  "workflow_id":"<workflow_id>",
  "run_id":"<run_id>""
}
```

Or using curl:

```bash
curl -X POST http://0.0.0.0:5001/api/event/end -H "Content-Type: application/json" -d '{"workflow_id": "<workflow_id>", "run_id": "<run_id>"}'
  -H "Content-Type: application/json"
```

## Project Structure

- `src/`: Main source code directory
  - `client.py`: Initializes the Restack client
  - `functions/`: Contains function definitions
  - `workflows/`: Contains workflow definitions
  - `services.py`: Sets up and runs the Restack services
  - `app.py`: Flask app to schedule and run workflows
