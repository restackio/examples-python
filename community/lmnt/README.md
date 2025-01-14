# Restack AI - LMNT Example

This repository contains a simple example project to help you scale with Restack AI.
It demonstrates how to scale reliably to millions of workflows on a local machine with LMNT voice generation.

## Motivation

When scaling AI workflows, you want to make sure that you can handle failures and retries gracefully.
This example demonstrates how to do this with Restack AI and LMNT's voice generation API.

### Workflow Steps

The table below shows the execution of 50 workflows in parallel, each with three steps.
Steps 2 is LMNT voice generation functions that must adhere to a rate limit of 1 concurrent call per second.

| Step | Workflow 1 | Workflow 2 | ... | Workflow 50 |
| ---- | ---------- | ---------- | --- | ----------- |
| 1    | Basic      | Basic      | ... | Basic       |
| 2    | LMNT       | LMNT       | ... | LMNT        |

### Traditional Rate Limit Management

When running multiple workflows in parallel, managing the rate limit for LMNT functions is crucial. Here are common strategies:

1. **Task Queue**: Use a task queue (e.g., Celery, RabbitMQ) to schedule LMNT calls, ensuring only one is processed at a time.
2. **Rate Limiting Middleware**: Implement middleware to queue requests and process them at the allowed rate.
3. **Semaphore or Locking**: Use a semaphore or lock to control access, ensuring only one LMNT function runs per second.

### With Restack

Restack automates rate limit management, eliminating the need for manual strategies. Define the rate limit in the service options, and Restack handles queuing and execution:

```python
client.start_service(
    task_queue="lmnt",
    functions=[lmnt_list_voices, lmnt_synthesize],
    options=ServiceOptions(
        rate_limit=1,
        max_concurrent_function_runs=1
    )
)
```

Focus on building your logics while Restack ensures efficient and resilient workflow execution.

### On Restack UI

You can see from the parent workflow how long each child workflow stayed in queue and how long was the execution time.

![Parent Workflow](./ui-parent.png)

And for each child workflow, for each step you can see how long the function stayed in queue, how long the function took to execute and how many retries happened.

![Child Workflow](./ui-child.png)

## Prerequisites

- Python 3.10 or higher
- Poetry (for dependency management)
- Docker (for running the Restack services)
- LMNT API key (sign up at https://www.lmnt.com)

## Prerequisites

- Docker (for running Restack)
- Python 3.10 or higher

## Start Restack

To start the Restack, use the following Docker command:

```bash
docker run -d --pull always --name restack -p 5233:5233 -p 6233:6233 -p 7233:7233 ghcr.io/restackio/restack:main
```

## Start python shell

```bash
poetry env use 3.10 && poetry shell
```

## Install dependencies

```bash
poetry install
```

```bash
poetry env info # Optional: copy the interpreter path to use in your IDE (e.g. Cursor, VSCode, etc.)
```

```bash
poetry run dev
```

## Run workflows

### from UI

You can run workflows from the UI by clicking the "Run" button.

![Run workflows from UI](./ui-endpoints.png)

### from API

You can run one workflow from the API by using the generated endpoint:

`POST http://localhost:6233/api/workflows/ChildWorkflow`

or multiple workflows by using the generated endpoint:

`POST http://localhost:6233/api/workflows/ExampleWorkflow`

### from any client

You can run workflows with any client connected to Restack, for example:

```bash
poetry run schedule
```

executes `schedule_workflow.py` which will connect to Restack and execute the `ChildWorkflow` workflow.

```bash
poetry run scale
```

executes `schedule_scale.py` which will connect to Restack and execute the `ExampleWorkflow` workflow.

```bash
poetry run interval
```

executes `schedule_interval.py` which will connect to Restack and execute the `ChildWorkflow` workflow every second.

## Deploy on Restack Cloud

To deploy the application on Restack, you can create an account at [https://console.restack.io](https://console.restack.io)

## Project Structure

- `src/`: Main source code directory
  - `client.py`: Initializes the Restack client
  - `functions/`: Contains function definitions
  - `workflows/`: Contains workflow definitions
  - `services.py`: Sets up and runs the Restack services
- `schedule_workflow.py`: Example script to schedule and run a workflow
- `schedule_interval.py`: Example script to schedule and a workflow every second
- `schedule_scale.py`: Example script to schedule and run 50 workflows at once

# Deployment

Create an account on [Restack Cloud](https://console.restack.io) and follow instructions on site to create a stack and deploy your application on Restack Cloud.