# USS Hornet Defense Tech Hackathon Quickstart: War Audio Denoise

[Everything you need for the USS Hornet Defense Tech Hackathon](https://lu.ma/uss-hornet-hackathon?tk=DNbUwU)

Tech stack used:

- Restack AI + Streamlit + FastAPI + SieveData

The AI workflow will need an audio file as an input and will denoise it to improve the quality of the audio.

## Datasets

Find audio samples at https://drive.google.com/drive/folders/1mbchTGfmhq2sc7sQEMfx-dQzd11kWIfO?usp=drive_link

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
   git clone https://github.com/restackio/examples-python.git
   cd examples/defense_quickstart_denoise
   ```

4. Setup virtual environment with Poetry:

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

5. Authenticate with SieveData (https://www.sievedata.com/functions/sieve/audio_enhancement/guide):

   ```bash
   poetry add sievedata
   sieve login
   ```

6. Run the services:

   ```bash
   poetry run services
   ```

7. In a new terminal, run FastAPI app:

   ```bash
   poetry shell
   ```

   ```bash
   poetry run app
   ```

8. In a new terminal, run the Streamlit frontend

   ```bash
   poetry run streamlit run frontend.py
   ```

# Deployment

Create an account on [Restack Cloud](https://console.restack.io) and follow instructions on site to create a stack and deploy your application on Restack Cloud.
