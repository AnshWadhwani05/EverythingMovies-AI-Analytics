# Multi-stage Dockerfile
# Stage 1: Build & Install dependencies
FROM python:3.9-slim as builder

WORKDIR /app

# Install system dependencies required for compiling some Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Stage 2: Runtime environment
FROM python:3.9-slim

WORKDIR /app

# Copy wheels from builder and install
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache /wheels/*

# Copy application source code
COPY src/ ./src/
COPY outputs/ ./outputs/
COPY data/ ./data/

# Expose API port
EXPOSE 8000

# Command to run the FastAPI application
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]