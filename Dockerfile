# Use Python 3.13 slim image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast Python package management
RUN pip install uv

# Copy uv configuration files
COPY pyproject.toml uv.lock ./

# Install Python dependencies
RUN uv sync --frozen

# Copy application code
COPY agent.py .
COPY .env.local .

# Expose port for health checks (optional)
EXPOSE 8080

# Set environment variables for uv
ENV PATH="/app/.venv/bin:$PATH"

# Run the LiveKit agent
CMD ["python", "agent.py", "start"]