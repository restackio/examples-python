# Restack AI Python SDK Examples

This repository contains various examples demonstrating how to use the Restack AI Python SDK. These examples are designed to help you get started with Restack AI and showcase different features and use cases.

## Examples

1. [Get Started](examples/get-started/README.md) - A simple example to help you get started with the Restack AI SDK.

## Prerequisites

- Python 3.8 or higher
- Poetry (for dependency management)

## Getting Started

1. Clone this repository:
   ```bash
   git clone https://github.com/restackio/examples-python
   cd examples-python
   ```

2. Navigate to the example you want to explore:
   ```bash
   cd examples/get-started
   ```

3. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

4. Follow the specific instructions in each example's README file.

## Running Restack in Docker

To run Restack locally using Docker, you have two options:

1. Using `docker run`:
   ```bash
   docker run -d --pull always --name studio -p 5233:5233 -p 6233:6233 -p 7233:7233 ghcr.io/restackio/engine:main
   ```

2. Using `docker-compose`:
   ```bash
   docker compose up -d --build --pull always
   ```

   This will force repulling and rebuilding.

After running either of these commands, the Restack UI will be available at http://localhost:5233

## Contributing

We welcome contributions to this repository! If you have an example you'd like to add or improvements to existing examples, please feel free to submit a pull request.