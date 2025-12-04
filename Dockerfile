# Use the official Python 3.12 slim image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Create a working directory
WORKDIR /app

# Copy the application files to the container
COPY . /app

# Install necessary dependencies including bash
RUN apt-get update && apt-get install -y \
    bash \
    build-essential \
    libffi-dev \
    curl \
    && pip install --upgrade pip \
    && pip install \
    schedule==1.2.0 \
    lxml==5.1.0 \
    pymongo==4.6.3 \
    python-dotenv==1.0.1 \
    requests==2.31.0 \
    aiohttp==3.9.5 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set bash as the default shell
SHELL ["/bin/bash", "-c"]

# Set the default command to run the script
CMD ["python", "main.py"]
