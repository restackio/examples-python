# Restack AI SDK - Gemini Generate Content Example

## Prerequisites

- Python 3.9 or higher
- Poetry (for dependency management)
- Set `GEMINI_API_KEY` as an environment variable from [Google AI Studio](https://aistudio.google.com)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/restackio/examples-python
   cd gemini_generate_content
   ```

2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

## Project Structure

- `src/`: Main source code directory
  - `client.py`: Initializes the Restack client
  - `functions/`: Contains function definitions
  - `workflows/`: Contains workflow definitions
  - `services.py`: Sets up and runs the Restack services
- `schedule_workflow.py`: Example script to schedule and run a workflow

## Usage

### Running the Services

To start the Restack services, run:

```bash
poetry run services
```

This will start the Restack service with the defined workflows and functions.

### Scheduling a Workflow

To schedule and run the example workflow, use:

```bash
poetry run schedule
```

This will schedule the `GeminiGenerateOppositeWorkflow` and print the result.