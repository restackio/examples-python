FROM python:3.9-slim

WORKDIR /app

# Install poetry
RUN pip install poetry

# Copy poetry files
COPY pyproject.toml poetry.lock* ./

# Copy application code
COPY src/ ./src/

# Configure poetry to not create virtual environment
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --no-dev --no-interaction --no-ansi

# Install supervisor
RUN apt-get update && apt-get install -y supervisor

# Create supervisor configuration
RUN echo "[supervisord]\n\
nodaemon=true\n\
\n\
[program:services]\n\
command=poetry run services\n\
stdout_logfile=/dev/stdout\n\
stdout_logfile_maxbytes=0\n\
stderr_logfile=/dev/stderr\n\
stderr_logfile_maxbytes=0\n\
\n\
[program:fastapi]\n\
command=poetry run app\n\
stdout_logfile=/dev/stdout\n\
stdout_logfile_maxbytes=0\n\
stderr_logfile=/dev/stderr\n\
stderr_logfile_maxbytes=0" > /etc/supervisor/conf.d/supervisord.conf

# Expose the port the app runs on
EXPOSE 8000

# Command to run supervisor which will manage both processes
CMD ["/usr/bin/supervisord"]