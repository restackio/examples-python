FROM python:3.12-slim

WORKDIR /app

# Combine apt installs to reduce layers
RUN apt-get update && apt-get install -y \
  libglib2.0-0 \
  libgl1-mesa-glx \
  && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml requirements.txt ./

COPY . .

# Install dependencies
RUN pip install -e .

# Expose port 80
EXPOSE 80

CMD ["python", "-m", "src.services"]
