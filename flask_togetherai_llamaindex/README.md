# Restack AI SDK - Flask + TogetherAI with LlamaIndex Example

## Prerequisites

- Python 3.9 or higher
- Poetry (for dependency management)
- Docker (for running the Restack services)
- Active [Together AI](https://together.ai) account with API key

## Usage

1. Run Restack local engine with Docker:

   ```bash
   docker run -d --pull always --name restack -p 5233:5233 -p 6233:6233 -p 7233:7233 ghcr.io/restackio/restack:main
   ```

2. Open the Web UI to see the workflows:

   ```bash
   http://localhost:5233
   ```

3. Clone this repository:

   ```bash
   git clone https://github.com/restackio/examples-python
   cd examples-python/examples/flask_togetherai_llamaindex
   ```

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

5. Set up your environment variables:

   Copy `.env.example` to `.env` and add your Together AI API key:

   ```bash
   cp .env.example .env
   # Edit .env and add your TOGETHER_API_KEY
   ```

6. Run the services:

   ```bash
   poetry run services
   ```

   This will start the Restack service with the defined workflows and functions.

7. In a new terminal, run flask app:

   ```bash
   poetry shell
   ```

   ```bash
   poetry run flask
   ```

8. Test your Api a POST request using curl:

   ```bash
   curl -X POST \
     http://localhost:5000/api/schedule \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Whats a cow?"}'
   ```

   This will schedule the Llamaindex workflow with simple prompt and return the result.
