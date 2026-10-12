# 🚀 AI-Powered DevOps Backend Container
# This creates a production-ready container for our FastAPI backend + AI engine

FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies for git, compilation, and health checks
RUN apt-get update && apt-get install -y \
    git \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend application
COPY . .

# Create directory for temporary workspaces (for GitHub cloning)
RUN mkdir -p /app/workspaces

# Set environment variables
ENV PYTHONPATH=/app
ENV WORKSPACE_PATH=/app/workspaces

# Expose port
EXPOSE 8000

# Health check to ensure the container is working
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Create a non-root user for security
RUN useradd --create-home --shell /bin/bash appuser
RUN chown -R appuser:appuser /app
USER appuser

# Run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]