FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src
RUN python -m pip install --no-cache-dir .

EXPOSE 8098

CMD ["python", "-m", "cola_skeleton.server", "--host", "0.0.0.0", "--port", "8098", "--db", "/data/notes.db"]
