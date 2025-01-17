# Restack AI - Gemini Example

This example demonstrates how to build reliable and scalable AI applications using Google's Gemini API with Restack. It shows how to handle rate limits, concurrent API calls, and workflow orchestration effectively.

We build four example workflows: a basic content generation workflow, a function calling workflow, a multi-function calling workflow, and a swarm workflow that demonstrates parallel execution.


## Motivation

When building AI applications with Gemini, you need to handle various production challenges:

1. **API Rate Limits**: Gemini API has concurrent request limits (e.g., 3 concurrent calls)([1](https://googleapis.github.io/python-genai)) that need to be managed across multiple workflows.

2. **Reliability**: AI workflows need retry mechanisms and graceful failure handling for production use.

3. **Scalability**: As your application grows to handle thousands of concurrent agents or requests, you need robust queue management and execution control.

### How Restack Helps

Restack provides built-in solutions for these challenges:

1. **Automated Rate Limiting**: Define rate limits in service options and let Restack handle the queuing:
```python
client.start_service(
    task_queue="gemini",
    functions=[generate_content, function_call],
    options=ServiceOptions(
        rate_limit=3,  # Match Gemini's concurrent call limit
        max_concurrent_function_runs=3
    )
)
```

2. **Built-in Retries**: Restack automatically handles retries and failure scenarios.

3. **Queue Management**: Efficiently manages thousands of concurrent workflows while respecting API limits.

## Prerequisites

- Python 3.9 or higher
- Poetry (for dependency management)
- Docker (for running the Restack services)
- Active [Google AI Studio](https://aistudio.google.com) account with API key

## Usage

1. Run Restack local engine with Docker:

   ```bash
   docker run -d --pull always --name restack -p 5233:5233 -p 6233:6233 -p 7233:7233 ghcr.io/restackio/restack:main
   ```

2. Open the web UI to see the workflows:

   ```bash
   http://localhost:5233
   ```

3. Clone this repository:

   ```bash
   git clone https://github.com/restackio/examples-python
   cd examples-python/community/gemini

4. Install dependencies using Poetry:

   ```bash
   poetry env use 3.12
   ```

   ```bash
   poetry shell
   ```

   ```bash
   poetry install
   ```

   ```bash
   poetry env info # Optional: copy the interpreter path to use in your IDE (e.g. Cursor, VSCode, etc.)
   ```

5. Set `GEMINI_API_KEY` as an environment variable from [Google AI Studio](https://aistudio.google.com)

   ```bash
   export GEMINI_API_KEY=<your-api-key>
   ```

6. Run the services in dev:

   ```bash
   poetry run dev
   ```

   This will start the Restack service with the defined workflows and functions.

8. Schedule workflows via the UI 

## Project Structure

- `src/`: Main source code directory
  - `client.py`: Initializes the Restack client
  - `functions/`: Contains function definitions
  - `workflows/`: Contains workflow definitions
  - `services.py`: Sets up and runs the Restack services
- `schedule_workflow.py`: Example script to schedule and run a workflow
