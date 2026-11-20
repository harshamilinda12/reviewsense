
FROM python:3.13-slim

WORKDIR /app

# Configure Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies
COPY requirements-api.txt .

RUN python -m pip install --no-cache-dir -r requirements-api.txt

# Create a non-root user
RUN groupadd -g 10001 appgroup && \
    useradd -m -u 10001 -g appgroup appuser

# Copy application code
COPY --chown=appuser:appgroup src/ ./src/

# Copy trained model
COPY --chown=appuser:appgroup models/ ./models/

# Switch to non-root user
USER appuser

EXPOSE 8000

# Start FastAPI
CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
