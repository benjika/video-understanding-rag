FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y ffmpeg && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

# Ensure /app/video exists
RUN mkdir -p /app/video

ENV PYTHONUNBUFFERED=1

CMD ["python", "app/main.py"]