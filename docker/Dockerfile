# MkDocs with nginx Docker image
# Base image: Python 3.11 slim for smaller image size
FROM python:3.11-slim

# Metadata
LABEL maintainer="link-check"
LABEL description="MkDocs documentation builder with nginx server"

# Update package manager
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        # Will add nginx and other packages in subsequent tasks
    && rm -rf /var/lib/apt/lists/*
