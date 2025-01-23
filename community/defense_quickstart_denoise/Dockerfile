FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y nginx

RUN pip install poetry

COPY pyproject.toml ./

COPY . .

# Configure poetry to not create virtual environment
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --no-interaction --no-ansi

# Copy Nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 80
EXPOSE 80

# Start Nginx, FastAPI, and Streamlit using Poetry
CMD service nginx start && \
  poetry run uvicorn src.app:app --host 0.0.0.0 --port 8000 & \
  poetry run streamlit run frontend.py --server.port=8501 & \
  poetry run services