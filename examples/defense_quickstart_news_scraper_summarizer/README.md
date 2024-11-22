# USS Hornet Defense Tech Hackathon Quickstart: War News Scraper & Summarizer

[Everything you need for the USS Hornet Defense Tech Hackathon](https://lu.ma/uss-hornet-hackathon?tk=DNbUwU)

Tech stack used:
- Restack AI + Streamlit + FastApi + OpenBabylon

The AI workflow will get RSS feed, crawl each article, translate it to English, summarize it & make a summary of the news found on RSS feed.

## Prerequisites

- Python 3.12 or higher
- Poetry (for dependency management)
- Docker (for running Restack services)

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
   cd examples/defense_quickstart_news_scraper_summarizer
   ```

4. Install dependencies using Poetry:

   ```bash
   poetry env use 3.12
   poetry shell
   poetry install
   poetry env info # Optional: copy the interpreter path to use in your IDE (e.g. Cursor, VSCode, etc.)
   ```

5. Set up your environment variables:

   Copy `.env.example` to `.env` and add your OpenBabylon API URL:

   ```bash
   cp .env.example .env
   # Edit .env and add your:
   # OPENBABYLON_API_URL
   # OPENAI_API_KEY - Set this to a random string as OpenBabylon uses OpenAI API
   ```

6. Run the services:

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
   poetry runstreamlit run frontend.py
   ```

10. You can test the API endpoint without the Streamlit UI with:

```bash
curl -X POST \
  http://localhost:8000/api/schedule \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.pravda.com.ua/rss/", "count": 5}'
```

This will schedule the workflow and return the result.
