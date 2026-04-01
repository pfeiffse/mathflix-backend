FROM python:3.11-slim

WORKDIR /app

# Kopiere requirements aus dem Repo-Root
COPY ../../requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

# Kopiere den Backend-Code aus dem Repo-Root
COPY ../../app /app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]