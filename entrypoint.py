#!/usr/bin/env python3
"""
Entrypoint script for the Docker container.
"""
import os
import subprocess
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Run the image processor with environment variables."""
    logger.info("Starting image processor entrypoint")
    
    # Environment variables with defaults
    input_dir = os.environ.get('INPUT_DIR', '/data/input')
    output_dir = os.environ.get('OUTPUT_DIR', '/data/output')
    config_file = os.environ.get('CONFIG_FILE', '/app/config/settings.yaml')
    sleep_interval = os.environ.get('SLEEP_INTERVAL', '10')
    
    logger.info(f"Input directory: {input_dir}")
    logger.info(f"Output directory: {output_dir}")
    logger.info(f"Config file: {config_file}")
    logger.info(f"Sleep interval: {sleep_interval} seconds")
    
    # Make sure directories exist
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    # Run the image processor
    cmd = [
        "python", "-m", "image_processor.main",
        "--input-dir", input_dir,
        "--output-dir", output_dir,
        "--config-file", config_file,
        "--sleep-interval", sleep_interval
    ]
    
    try:
        logger.info(f"Executing: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Error running image processor: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Received interrupt signal, shutting down...")
        sys.exit(0)

if __name__ == "__main__":
    main()
