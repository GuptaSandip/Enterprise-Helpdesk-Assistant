# ==========================================
# Stage 1: Build the React Frontend
# ==========================================
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend

# Copy dependencies definitions
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci

# Copy frontend source code
COPY frontend/ ./

# Build the React app (outputs to ../static due to outDir configuration in vite.config.js)
RUN npm run build

# ==========================================
# Stage 2: Build the FastAPI Backend Server
# ==========================================
FROM python:3.12-slim AS backend-runner
WORKDIR /app

# Install system dependencies if any
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy pyproject.toml and install dependencies
COPY pyproject.toml ./
RUN pip install --no-cache-dir .

# Copy backend application code
COPY app/ ./app/
COPY main.py ./

# Copy built frontend assets from Stage 1 into /app/static
COPY --from=frontend-builder /app/static ./static

# Expose backend port (FastAPI serves both API and frontend static files)
EXPOSE 8000

# Set environment variables defaults
ENV PORT=8000
ENV HOST=0.0.0.0

# Start Uvicorn server
CMD ["sh", "-c", "uvicorn main:app --host $HOST --port $PORT"]
