# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies required for PostgreSQL and Pillow
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    python3-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . /app/

# Create all media subdirectories and make entrypoint executable
RUN mkdir -p /app/staticfiles \
    /app/media/products \
    /app/media/products/thumbs \
    /app/media/categories \
    /app/media/hero \
    /app/media/brands \
    /app/media/profiles \
    && chmod +x /app/entrypoint.sh

# Run entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]

# Expose port (Gunicorn will run here)
EXPOSE 8000
