FROM ghcr.io/astral-sh/uv:python3.10-bookworm-slim

WORKDIR /app

COPY pyproject.toml ./

COPY . .

# Install dependencies
RUN uv sync --no-dev

# Expose port 80
EXPOSE 80

CMD ["uv", "run", "services"]

