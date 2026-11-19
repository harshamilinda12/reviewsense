
# 1. Start with an official Python image
FROM python:3.13-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Configure Python for container execution
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 4. Copy dependency requirements
COPY requirements-api.txt .

# 5. Install Python dependencies
RUN python -m pip install --no-cache-dir -r requirements-api.txt

# 6. Copy the backend application
COPY src/ ./src/

# 7. Copy the trained model
COPY models/ ./models/

# 8. Document the API port
EXPOSE 8000

# 9. Start the FastAPI server
CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
