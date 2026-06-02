# Use a lightweight, modern Python base image
FROM python:3.12-slim

# Install system dependencies needed for Git operations
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

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

# Expose port 7860 for Gradio (Hugging Face Spaces requirement)
# FastAPI runs internally on 8000
EXPOSE 7860

# Run the combined FastAPI + Gradio app
# app.py starts both in one process: FastAPI in a background thread + Gradio UI on port 7860
CMD ["uv", "run", "python", "src/unity_repo_analyzer/app.py"]
