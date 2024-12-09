# Restack AI - Audio transcript and translation example

This example showcases how to transcribe an mp3 audio and then later translate the generated text to a target language, all done in a single workflow defined with Restack AI.


## Prerequisites

- Python 3.10 or higher
- Poetry (for dependency management)
- Docker (for running the Restack services)

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
   cd examples-python/examples/get-started
   ```
  
4. Create .env file with: STRIPE_SECRET_KEY and OPENAI_API_KEY

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

5. Run the services:

   ```bash
   poetry run services
   ```

   This will start the Restack service with the defined workflows and functions.

6. In a new terminal, schedule the workflow:

   ```bash
   poetry shell
   ```

   ```bash
   poetry run schedule
   ```

   This will schedule the `TranscribeTranslateWorkflow` and print the result.
