# Use the official Python 3.13 Alpine image as the base image
FROM python:3.13-alpine

# Set the maintainer's contact information
LABEL maintainer="volodymyr.vinohradov@gmail.com"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    UV_PROJECT_ENVIRONMENT="/usr/local/"

RUN apk add --no-cache gcc musl-dev linux-headers

# Set the working directory inside the container
WORKDIR /app

# Copy dependency files into the container
COPY pyproject.toml uv.lock ./

# Install dependencies, sync with uv, and clean up unnecessary files
RUN pip install --no-cache-dir uv \
    && uv --no-cache-dir sync

# Copy the rest of the application code into the container
COPY . .

# Create necessary directories, set permissions, and make entrypoint executable
RUN adduser --disabled-password --home /home/socuser socuser && \
    mkdir -p /files/profile /files/static && \
    chown -R socuser:socuser /files /home/socuser && \
    chmod -R 755 /files /home/socuser


EXPOSE 8000
# Switch to the non-root user
USER socuser
