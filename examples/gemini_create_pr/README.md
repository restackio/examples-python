# Restack AI SDK - Gemini Generate Content Example

## Prerequisites

- Python 3.9 or higher
- Poetry (for dependency management)
- Docker (for running the Restack services)
- Active [Google AI Studio](https://aistudio.google.com) account with API key
- GitHub personal access token with repo permissions

1. Run Restack local engine with Docker:
   ```bash
   docker run -d --pull always --name studio -p 5233:5233 -p 6233:6233 -p 7233:7233 ghcr.io/restackio/engine:main
   ```

2. Open the web UI to see the workflows:

   ```bash
   http://localhost:5233
   ```

3. Clone this repository:
   ```bash
   git clone https://github.com/restackio/examples-python
   cd examples-python/examples/gemini_create_pr
   ```

4. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

5. Set `GEMINI_API_KEY` as an environment variable from [Google AI Studio](https://aistudio.google.com)

   ```bash
   export GEMINI_API_KEY=<your-api-key>
   ```

6. Set `GITHUB_TOKEN` as an environment variable from your GitHub account

   ```bash
   export GITHUB_TOKEN=<your-github-token>
   ```

7. Run the services:

   ```bash
   poetry run services
   ```

   This will start the Restack service with the defined workflows and functions.

8. In a new terminal, schedule the workflow:

   ```bash
   python run_ui.py
   ```

   This will open a Streamlit UI to run the example.

## Project Structure

- `src/`: Main source code directory
  - `client.py`: Initializes the Restack client
  - `functions/`: Contains function definitions
    - `util/`: Utility functions
  - `workflows/`: Contains workflow definitions
  - `ui/`: Streamlit UI files
  - `services.py`: Sets up and runs the Restack services
- `run_ui.py`: Example script to run the UI