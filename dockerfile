# Use a lightweight, modern Python base image
FROM python:3.12-slim

# Install system dependencies needed for Git operations
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /lib/apt/lists/*

# Install uv directly into the container architecture
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set up our application directory
WORKDIR /app

# Copy dependency definition files first to leverage Docker caching
COPY pyproject.toml uv.lock ./

# Install project dependencies using uv sync
RUN uv sync --frozen --no-cache

# Copy the rest of your source code into the container
COPY . .

# Hugging Face Spaces strictly requires applications to expose port 7860
EXPOSE 7860

# Run Uvicorn pointing directly to the Hugging Face required port configuration
CMD ["uv", "run", "uvicorn", "src.unity_repo_analyzer.server:app", "--host", "0.0.0.0", "--port", "7860"]