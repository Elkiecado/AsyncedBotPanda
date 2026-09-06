FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .


ENV PYTHONUNBUFFERED=1

RUN useradd --create-home --shell /bin/bash appuser
RUN mkdir -p /app/data && chown -R appuser:appuser /app
USER appuser

CMD ["python", "-m", "app.main"]