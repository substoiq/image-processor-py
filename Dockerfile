FROM python:3.9-slim

# Install required packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    findutils \
    curl \
    libheif-dev \
    && rm -rf /var/lib/apt/lists/*

# Set up working directories
WORKDIR /app
RUN mkdir -p /data/input /data/output

# Copy project definition and install dependencies
COPY pyproject.toml .
COPY image_processor/ ./image_processor/
RUN pip install --no-cache-dir .

# Copy application files
COPY entrypoint.py .
COPY config/ ./config/

# Make Python scripts executable
RUN chmod +x entrypoint.py

# Set environment variables
ENV INPUT_DIR=/data/input \
    OUTPUT_DIR=/data/output \
    CONFIG_FILE=/app/config/settings.yaml \
    SLEEP_INTERVAL=10

# Run the image processor
ENTRYPOINT ["python", "/app/entrypoint.py"]