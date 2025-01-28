FROM python:3.12-slim

WORKDIR /app

# Combine apt installs to reduce layers
RUN apt-get update && apt-get install -y \
  libglib2.0-0 \
  libgl1-mesa-glx \
  && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install poetry in the same step to reuse the base layer
RUN pip install poetry \
  && poetry config virtualenvs.create false

COPY pyproject.toml ./

COPY . .

# Install dependencies
RUN poetry install --no-interaction --no-ansi

# Expose port 80
EXPOSE 80

CMD poetry run python -m src.services
