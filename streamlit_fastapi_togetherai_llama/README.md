# Restack AI SDK - Streamlit + FastApi + TogetherAI with LlamaIndex Example

The model will act as a pirate and you can send it prompts from the streamlit ui and get responses. This will showcase how a streamlit app can easily communicate to models using a fastapi server with Restack ai library.

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
   cd examples-python/examples/fastapi_togetherai_llama
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

7. In a new terminal, run fastapi app:

   ```bash
   poetry shell
   ```

   ```bash
   poetry run app
   ```

8. In a new terminal, run the streamlit frontend

   ```bash
   poetry run streamlit run frontend.py
   ```

9. You can test api endpoint without the streamlit UI with:

   ```bash
   curl -X POST \
     http://localhost:8000/api/schedule \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Tell me a short joke"}'
   ```

   This will schedule the Llamaindex workflow with simple prompt and return the result.
