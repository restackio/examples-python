FROM ghcr.io/astral-sh/uv:python3.10-bookworm-slim AS builder

ARG SUB_PATH

WORKDIR /app

COPY --from=pullrepo /app/repo .

WORKDIR /app${SUB_PATH:+/$SUB_PATH}

#Install dependencies
RUN uv sync --no-dev

# Expose port 80
EXPOSE 80

CMD ["uv", "run", "services"]
