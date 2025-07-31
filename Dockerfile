FROM python:3.11-slim

# Install dependencies needed for the wait command and psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev gcc && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app
RUN pip install gunicorn
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .