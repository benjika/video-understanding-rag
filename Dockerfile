FROM python:3.10-slim-bullseye

# Upgrade system packages and install ffmpeg in one layer
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

# Install Python dependencies
RUN python -m pip install --upgrade pip && \
    python -m pip install --no-cache-dir -r requirements.txt

COPY . .

# Ensure /app/video exists (but you also mount it as a volume)
RUN mkdir -p /app/video

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]