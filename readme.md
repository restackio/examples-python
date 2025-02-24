# Restack AI Python Examples

This repository contains various examples demonstrating how to use the Restack AI Python SDK. These examples are designed to help you get started with Restack AI and showcase different features and use cases.

This repository is organized into two sections:

- [Official examples](/): Actively maintained and tested by the Restack team
- [Community](/community) examples: Contributed by the community and may not be regularly updated

## Prerequisites

- Python 3.12 or higher
- Uv (for dependency management)

## Getting Started

1. Clone this repository:

   ```bash
   git clone https://github.com/restackio/examples-python
   cd examples-python
   ```

2. Navigate to the example you want to explore:

   ```bash
   cd examples-python/<example-name>
   ```

3. Follow the specific instructions in each example's README file.

## Running Restack in Docker

To run Restack locally using Docker, you have two options:

Using `docker run`:

```bash
docker run -d --pull always --name restack -p 5233:5233 -p 6233:6233 -p 7233:7233 -p 9233:9233 ghcr.io/restackio/restack:main
```

This will force repulling and rebuilding.

After running either of these commands, the Restack UI will be available at http://localhost:5233

## Contributing

We welcome contributions to this repository. If you have an example you'd like to add or improvements to existing examples, please feel free to submit a pull request.
