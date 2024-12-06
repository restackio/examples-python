# Restack AI - Production Example

This repository contains a simple example project to help you scale with the Restack AI.
It demonstrates how to scale reliably to millions of workflows on a local machine with a local LLM provider.

## Prerequisites

- Python 3.8 or higher
- Poetry (for dependency management)
- Docker (for running the Restack services)
- Local LLM provider (we use LMStudio and a Meta Llama 3.1 8B Instruct 4bit model in this example)

## Usage

0. Start LM Studio and start local server with Meta Llama 3.1 8B Instruct 4bit model

https://lmstudio.ai

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
   cd examples-python/examples/production_demo
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

5. Run the services:

   ```bash
   poetry run dev
   ```

   This will start the Restack service with the defined workflows and functions.

6. In a new terminal, schedule the workflow:

   ```bash
   poetry shell
   ```

   ```bash
   poetry run workflow
   ```

   This will schedule the ExampleWorkflow` and print the result.

7. Optionally, schedule the workflow to run on a interval:

   ```bash
   poetry run interval
   ```

8. Optionally, schedule a parent workflow to run 100 child workflows all at once:

   ```bash
   poetry run scale
   ```

## Project Structure

- `src/`: Main source code directory
  - `client.py`: Initializes the Restack client
  - `functions/`: Contains function definitions
  - `workflows/`: Contains workflow definitions
  - `services.py`: Sets up and runs the Restack services
- `schedule_workflow.py`: Example script to schedule and run a workflow
- `schedule_interval.py`: Example script to schedule and a workflow every second
- `schedule_scale.py`: Example script to schedule and run 100 workflows at once
