# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all scripts to the container
COPY . .

# Default command to run the entrypoint script
CMD ["python3", "run_all.py"]
