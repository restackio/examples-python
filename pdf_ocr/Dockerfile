FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# Combine apt installs to reduce layers
RUN apt-get update && apt-get install -y --no-install-recommends\
  libglib2.0-0 \
  libgl1-mesa-glx \
  && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml requirements.txt ./

COPY . .

# Install dependencies
RUN uv sync --frozen --no-dev

# Expose port 80
EXPOSE 80

CMD ["uv", "run", "services"]
