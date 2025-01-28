FROM python:3.12-slim

WORKDIR /app

# Install necessary system packages
RUN apt-get update && apt-get install -y \
  libglib2.0-0 \
  libgl1-mesa-glx \
  && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir poetry

# Set custom index URL for PyTorch in Poetry
RUN poetry config repositories.pytorch https://download.pytorch.org/whl/cpu

# Ensure Poetry doesn't create virtual environments
RUN poetry config virtualenvs.create false

# Copy only dependency files first (for caching)
COPY pyproject.toml poetry.lock ./

# Install dependencies with extra index URL for PyTorch
RUN poetry install --no-interaction --no-ansi --no-cache \
  --source pytorch

# Copy the rest of the application code
COPY . .

# Expose port
EXPOSE 80

CMD poetry run python -m src.services
