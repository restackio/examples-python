# Quickstart USS Hornet Defense Tech Hackathon

[Everything you need for the USS Hornet Defense Tech Hackathon](https://lu.ma/uss-hornet-hackathon?tk=DNbUwU)

Restack AI - Streamlit + FastApi + OpenBabylon Example

The AI workflow will get rss feed, crawl each article, translate it to english, summarize it and make a summary of the news found on rss feed.

## Prerequisites

- Python 3.12 or higher
- Poetry (for dependency management)
- Docker (for running the Restack services)

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
   cd examples/defense_quickstart
   ```

4. Install dependencies using Poetry:

   ```bash
   poetry install
   ```

5. Set up your environment variables:

   Copy `.env.example` to `.env` and add your OpenBabylon API URL:

   ```bash
   cp .env.example .env
   # Edit .env and add your OPENBABYLON_API_URL
   ```

6. Open poetry shell:

   ```bash
   poetry shell
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
  -d '{"url": "https://www.pravda.com.ua/rss/", "count": 5}'
```

This will schedule the workflow and return the result.
