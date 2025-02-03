FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y

COPY pyproject.toml requirements.txt ./

COPY . .

# Install dependencies
RUN pip install -e .

# Expose port 80
EXPOSE 80

CMD ["python", "-m", "src.services"]
