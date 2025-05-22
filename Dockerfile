FROM python:3.10-slim-bullseye

# Upgrade system packages to address vulnerabilities
RUN apt-get update && apt-get upgrade -y

RUN sed -i 's|http://deb.debian.org|http://ftp.de.debian.org|g' /etc/apt/sources.list

WORKDIR /app

COPY requirements.txt .

RUN apt-get update
RUN apt-get install -y ffmpeg
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

# Ensure /app/video exists
RUN mkdir -p /app/video

ENV PYTHONUNBUFFERED=1

CMD ["python", "app/main.py"]