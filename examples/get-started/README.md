# Restack AI SDK - Get Started Example

This repository contains a simple example project to help you get started with the Restack AI SDK. It demonstrates how to set up a basic workflow and functions using the SDK.

## Prerequisites

- Python 3.8 or higher
- Poetry (for dependency management)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/restackio/examples-python
   cd examples-python
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

This will schedule the "GreetingWorkflow" and print the result.

## Workflow and Functions

The example includes a simple "GreetingWorkflow" with two functions:

1. `welcome`: Greets a person
2. `goodbye`: Says goodbye to a person