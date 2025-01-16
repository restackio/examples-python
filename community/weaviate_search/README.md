# Restack AI SDK with Weaviate - Get Started Example

This repository contains a simple example project to help you get started with the Restack AI SDK and Weaviate. It demonstrates how to set up a basic workflow and functions using the Restack AI SDK to interact with a Weaviate vector database.

The example is a follow along of <https://weaviate.io/developers/weaviate/starter-guides/custom-vectors> and includes:

- Setting up a Weaviate client
- Seeding a Weaviate database with Jeopardy questions
- Performing vector searches using Restack AI functions

## Prerequisites

- Python 3.9 or higher
- Poetry (for dependency management)

## Installation

2. Install dependencies using Poetry:

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

To use this project, you need to have access to Weaviate Cloud. Follow these steps to obtain your `WEAVIATE_URL` and `WEAVIATE_API_KEY`:

1. **Sign up for Weaviate Cloud**: If you haven't already, create an account on [Weaviate Cloud](https://console.weaviate.cloud).
2. **Create a Weaviate Instance**: Once logged in, create a new Weaviate instance.
3. **Retrieve Credentials**: After your instance is set up, navigate to the instance details page to find your `WEAVIATE_URL` and `WEAVIATE_API_KEY`.

Add these credentials to your `.env` file.

## Usage

### Start Restack Engine

Using `docker run`:

```bash
docker run -d --pull always --name restack -p 5233:5233 -p 6233:6233 -p 7233:7233 ghcr.io/restackio/restack:main
```

### Running the Services

To start the Restack services, run:

```bash
poetry run services
```

This will start the Restack service with the defined workflows and functions.

### Scheduling Workflows

To schedule and run the example workflows, use:

```bash
poetry shell
```

```bash
poetry run schedule-seed-workflow
```

This will schedule the "SeedWorkflow" and print the result.

To run the search workflow, use:

```bash
poetry run schedule-search-workflow
```

This will schedule and execute the search workflow, allowing you to perform searches on your Weaviate instance.
