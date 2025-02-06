FROM ghcr.io/restackio/uv-torch:main

WORKDIR /app

COPY pyproject.toml requirements.txt ./

COPY . .

# Install dependencies
RUN uv sync --no-dev

# Expose port 80
EXPOSE 80

CMD ["uv", "run", "services"]
