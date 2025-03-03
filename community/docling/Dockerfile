FROM python:3.12-bookworm

WORKDIR /app

RUN apt-get update && apt-get install -y \
    git build-essential gcc libc-dev \
    && apt-get clean

RUN pip install --no-cache-dir --timeout=60 --retries=5 poetry

COPY pyproject.toml ./

COPY . .

# Configure poetry to not create virtual environment
RUN poetry config virtualenvs.create false

ENV PIP_EXTRA_INDEX_URL=https://download.pytorch.org/whl/cpu

# Install dependencies
RUN poetry install --no-interaction --no-ansi

# Expose port 80
EXPOSE 80

CMD poetry run python -m src.services