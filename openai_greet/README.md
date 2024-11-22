# Restack AI SDK - OpenAI Greet Example

## Prerequisites

- Python 3.8 or higher
- Poetry (for dependency management)
- Docker (for running the Restack services)
- Active [OpenAI](https://platform.openai.com) account with API key

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
   cd examples-python/examples/openai_greet
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

5. Set `OPENAI_API_KEY` as an environment variable from [OpenAI](https://platform.openai.com)

   ```bash
   export OPENAI_API_KEY=<your-api-key>
   ```

6. Run the services:

   ```bash
   poetry run services
   ```

   This will start the Restack service with the defined workflows and functions.

7. In a new terminal, schedule the workflow:

   ```bash
   poetry shell
   ```

   ```bash
   poetry run schedule
   ```

   This will schedule the `OpenaiGreetWorkflow` and print the result.

## Project Structure

- `src/`: Main source code directory
  - `client.py`: Initializes the Restack client
  - `functions/`: Contains function definitions
  - `workflows/`: Contains workflow definitions
  - `services.py`: Sets up and runs the Restack services
- `schedule_workflow.py`: Example script to schedule and run a workflow
