# USS Hornet Defense Tech Hackathon Quickstart: War Audio Transcription & Translation

[Everything you need for the USS Hornet Defense Tech Hackathon](https://lu.ma/uss-hornet-hackathon?tk=DNbUwU)

Tech stack used:

- Restack AI + Streamlit + FastApi + Groq + OpenBabylon

The AI workflow will need an audio file as an input and will transcribe it & translate it to English.

## Datasets

Find audio samples at https://drive.google.com/drive/folders/1mbchTGfmhq2sc7sQEMfx-dQzd11kWIfO?usp=drive_link

## OpenBabylon credentials

During the hackathon, OpenBabylon provided a public url:

OPENBABYLON_API_URL=http://64.139.222.109:80/v1

## Prerequisites

- Python 3.12 or higher
- Uv (for dependency management)
- Docker (for running Restack services)

## Usage

1. Run Restack local engine with Docker:

   ```bash
   docker run -d --pull always --name restack -p 5233:5233 -p 6233:6233 -p 7233:7233 -p 9233:9233 ghcr.io/restackio/restack:main
   ```

2. Open the Web UI to see the workflows:

   ```bash
   http://localhost:5233
   ```

3. Clone this repository:

   ```bash
   git clone https://github.com/restackio/examples-python.git
   cd examples/defense_quickstart_audio_transcription_translation
   ```

4. Setup virtual environment with Uv:

   ```bash
   uv venv && source .venv/bin/activate
   ```

```bash
 uv sync
```

5. Set up your environment variables:

   Copy `.env.example` to `.env` and add your OpenBabylon API URL:

   ```bash
   cp .env.example .env
   # Edit .env and add your:
   # OPENBABYLON_API_URL
   # GROQ_API_KEY
   ```

6. Run the services:

   ```bash
   uv run services
   ```

   This will start the Restack service with the defined workflows and functions.

7. In a new terminal, run FastAPI app:

   ```bash
   uv venv && source .venv/bin/activate
   ```

   ```bash
   uv run app
   ```

8. In a new terminal, run the Streamlit frontend

   ```bash
   uv run streamlit run frontend.py
   ```

# Deployment

Create an account on [Restack Cloud](https://console.restack.io) and follow instructions on site to create a stack and deploy your application on Restack Cloud.
