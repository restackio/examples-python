FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

COPY . .

RUN apt-get update && \
    apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

#Install dependencies
RUN uv sync --no-dev

# Run the application.
CMD ["uv", "run", "python", "src/agent.py", "start"]