# Quickstart Llama Hackathon

[Everything you need for the Llama Impact Hackathon](https://docs.restack.io/community/hackathons/08-11-2024-llama-impact)

Restack AI - Streamlit + FastApi + TogetherAI with LlamaIndex Example

The AI workflow will search hacker news based on a query, crawl each project's website, and make summaries for the user.

## Prerequisites

- Python 3.12 or higher
- Poetry (for dependency management)
- Docker (for running the Restack services)
- Active [Together AI](https://together.ai) account with API key

## YouTube walkthrough

[![Hackathon Walkthrough](https://img.youtube.com/vi/EgiYVXmnalU/0.jpg)](https://www.youtube.com/watch?v=EgiYVXmnalU)

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
   cd examples-python/examples/llama_quickstart
   ```

4. 

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

6. Open poetry shell:

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

It will display an interpreter path like
...caches/pypoetry/virtualenvs/get-started-ORuVhULK-py3.12

When you open a python file in VSCode or other IDEs like Cursor, you can select the interpreter path to use the poetry environment.

7. Run the services:

   ```bash
   poetry run services
   ```

   This will start the Restack service with the defined workflows and functions.

8. In a new terminal, run FastAPI app:

   ```bash
   poetry shell
   ```

   ```bash
   poetry run app
   ```

9. In a new terminal, run the Streamlit frontend

   ```bash
   poetry run streamlit run frontend.py
   ```

10. You can test the API endpoint without the Streamlit UI with:

```bash
curl -X POST \
  http://localhost:8000/api/schedule \
  -H "Content-Type: application/json" \
  -d '{"query": "AI", "count": 5}'
```

This will schedule the workflow and return the result.
