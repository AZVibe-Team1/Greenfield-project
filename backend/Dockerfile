# Backend Dockerfile for Job Portal API
# This Dockerfile sets up a Python 3.12+ environment with FastAPI and uv package manager

# Use Python 3.12 slim image as base
# Slim images reduce image size while maintaining functionality
FROM python:3.12-slim

# Set working directory inside the container
# All subsequent commands will run from this directory
WORKDIR /app

# Set environment variables
# Prevents Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies required for building Python packages
# - build-essential: Compiler tools (gcc, g++, make)
# - curl: For downloading uv installer and health checks
# - git: May be needed for some Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install uv - fast Python package installer and resolver
# uv is used for dependency management in this project
# RUN curl -LsSf https://astral.sh/uv/install.sh | sh
# ENV PATH="/root/.cargo/bin:$PATH"
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/


# Copy dependency files first for better Docker layer caching
# This allows Docker to cache dependencies separately from code changes
COPY pyproject.toml ./

# Install Python dependencies using uv
# uv sync installs all dependencies from pyproject.toml
# COPY uv.lock ./
# RUN uv sync --frozen
RUN uv sync

# Copy the rest of the backend application code
# This is done after dependency installation to leverage Docker cache
# COPY backend/ ./backend/

# Expose port 8000 - default FastAPI/Uvicorn port
# This port will be mapped to host machine in docker-compose.yml
EXPOSE 8000

# Set the default command to run the FastAPI application
# Using uv run to ensure dependencies are available
# Uvicorn will be started with hot-reload in development
CMD ["uv", "run", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

