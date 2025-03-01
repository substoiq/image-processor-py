# Image Processor

A containerized utility that monitors directories for images, processes them according to configuration settings, and saves them with standardized names.

## Features

- **Monitors Folders**: Continuously watches input directories for new images
- **Configurable Settings**: Control image dimensions, format, and quality
- **Smart Renaming**: Produces sequentially numbered outputs with timestamps
- **Multiple Format Support**: Handles common image formats (JPG, PNG, GIF, HEIC, etc.)
- **Docker & Kubernetes Ready**: Run anywhere with containerization
- **Modern Python Package**: Structured as a proper Python package with pyproject.toml

## Quick Start

### Docker Compose

```bash
# Clone the repository
git clone https://github.com/yourusername/image-processor.git
cd image-processor

# Start the container
docker-compose up -d

# Add images to process
cp your-images/*.jpg data/input/

# Check processed results
ls -la data/output/
```

### Custom Configuration

Edit `config/settings.yaml`:

```yaml
image:
  format: "jpg"  # Output format (jpg, png, webp, etc.)
  width: 800     # Output width in pixels
  height: 600    # Output height in pixels
  quality: 85    # Quality setting (1-100)
```

## Installation

### Prerequisites

- Docker and Docker Compose for local usage
- Kubernetes cluster for production deployment
- Python 3.9+ for development

### Local Development Setup

```bash
# Create development environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install package
pip install -e .

# Run directly
python -m image_processor.main --input-dir ./data/input --output-dir ./data/output
```

## Kubernetes Deployment

```bash
# Apply Kubernetes manifests
kubectl apply -f kubernetes-manifests.yaml

# Check deployment status
kubectl get pods -l app=image-processor
```

## Extended Format Support

For HEIC/HEIF (Apple) image support:

1. Install system dependencies (already in Dockerfile):
   ```shell
   apt-get install -y libheif-dev
   ```

2. Add Python dependency (already in pyproject.toml):
   ```shell
   pillow-heif>=0.10.0
   ```

## Project Structure

```
image-processor/
├── image_processor/        # Python package
│   ├── __init__.py
│   └── main.py             # Main processing code
├── config/
│   └── settings.yaml       # Configuration file
├── data/                   # Local data directories
│   ├── input/              # Place images here
│   └── output/             # Processed images appear here
├── pyproject.toml          # Python package definition
├── Dockerfile              # Container definition
├── docker-compose.yml      # Local development setup
└── kubernetes-manifests.yaml  # Kubernetes deployment
```

## Building and Pushing Images

```bash
# Build the image
docker build -t image-processor:latest .

# Tag for registry
docker tag image-processor:latest yourusername/image-processor:latest

# Push to registry
docker push yourusername/image-processor:latest
```

## License

[Your License Information]
