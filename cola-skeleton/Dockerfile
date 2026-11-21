FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app
COPY . /app

EXPOSE 8098
CMD ["python", "server.py", "--host", "0.0.0.0", "--port", "8098", "--db", "/data/notes.db"]
