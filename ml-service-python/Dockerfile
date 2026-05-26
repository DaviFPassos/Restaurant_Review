# Use lightweight Python 3.12 slim image as base
FROM python:3.12-slim

# Prevent Python from writing bytecode files to disk (saves space)
# and force direct output to terminal (important for container logs)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install minimal system dependencies
# build-essential is needed for compiling C extensions in TensorFlow and other packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies first (for build cache optimization)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy API code and ML artifacts (.keras model and label encoder pickle file)
COPY . .

# Expose FastAPI service port
EXPOSE 8000

# Run Uvicorn ASGI server in production mode
# --host 0.0.0.0 allows external connections to the container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

