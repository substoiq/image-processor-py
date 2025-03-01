#!/usr/bin/env python3
"""
Image Processor - Monitors a directory for new images and processes them
according to settings defined in a YAML file.
"""
import os
import time
import logging
import glob
import yaml
from datetime import datetime
# import shutil
from pathlib import Path
import argparse
from PIL import Image

# Add support for HEIC format
try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
    HEIC_SUPPORT = True
except ImportError:
    HEIC_SUPPORT = False
    logging.warning("pillow-heif not installed. HEIC format will not be supported.")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Process images from a input directory to an output directory.')
    parser.add_argument('--input-dir', default=os.environ.get('INPUT_DIR', '/data/input'),
                        help='Directory to monitor for new images')
    parser.add_argument('--output-dir', default=os.environ.get('OUTPUT_DIR', '/data/output'),
                        help='Directory to save processed images')
    parser.add_argument('--config-file', default=os.environ.get('CONFIG_FILE', '/app/config/settings.yaml'),
                        help='Path to configuration file')
    parser.add_argument('--sleep-interval', type=int, default=int(os.environ.get('SLEEP_INTERVAL', 10)),
                        help='Sleep interval between checks (seconds)')
    return parser.parse_args()

def load_config(config_file):
    """Load configuration from YAML file."""
    try:
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        logger.info(f"Loaded configuration from {config_file}")
        return config
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
        # Return default configuration if file cannot be loaded
        return {
            'image': {
                'format': 'jpg',
                'width': 800,
                'height': 600,
                'quality': 85
            }
        }

def process_image(input_file, output_file, config):
    """Process an image according to configuration."""
    try:
        # Open the image
        with Image.open(input_file) as img:
            # Resize the image
            img = img.resize((config['image']['width'], config['image']['height']), Image.LANCZOS)
            
            # Get the format - normalize to uppercase and handle jpg/jpeg properly
            format_name = config['image']['format'].upper()
            # Convert 'JPG' to 'JPEG' as Pillow uses JPEG, not JPG
            if format_name == 'JPG':
                format_name = 'JPEG'
            
            # Save the image with specified quality
            img.save(output_file, format=format_name, 
                   quality=config['image']['quality'])
        
        logger.info(f"Processed {input_file} -> {output_file}")
        return True
    except Exception as e:
        logger.error(f"Error processing image {input_file}: {e}")
        return False

def find_next_available_number(output_dir, format_ext):
    """Find the next available number for output filename."""
    counter = 1
    while counter < 1000:
        padded_counter = f"{counter:02d}"
        # Check if any file with this number exists
        matching_files = glob.glob(os.path.join(output_dir, f"foto-{padded_counter}-*.{format_ext}"))
        if not matching_files:
            return counter
        counter += 1
    
    # If we reach 1000, just use timestamp only
    return None

def process_files(input_dir, output_dir, config, processed_marker_dir=None):
    """Process all new image files in the input directory."""
    if processed_marker_dir is None:
        processed_marker_dir = output_dir
        
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Get image format from config
    image_format = config['image']['format'].lower()
    
    # Get all files in the input directory
    for filename in os.listdir(input_dir):
        input_file = os.path.join(input_dir, filename)
        
        # Skip if not a file
        if not os.path.isfile(input_file):
            continue
            
        # Check if it's an image file (case-insensitive)
        ext = os.path.splitext(filename)[1].lower()
        supported_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
        
        # Add HEIC extensions if supported
        if HEIC_SUPPORT:
            supported_extensions.extend(['.heic', '.heif'])
            
        if ext not in supported_extensions:
            continue
            
        # Skip already processed files
        marker_file = os.path.join(processed_marker_dir, f".processed_{filename}")
        
        if os.path.exists(marker_file):
            continue
            
        logger.info(f"Processing {filename}")
        
        # Find next available number
        counter = find_next_available_number(output_dir, image_format)
        current_datetime = datetime.now().strftime("%Y%m%d-%H%M%S")
        
        if counter is not None:
            new_filename = f"foto-{counter:02d}-{current_datetime}.{image_format}"
        else:
            # If no number is available, use just datetime
            new_filename = f"foto-{current_datetime}.{image_format}"
            
        output_file = os.path.join(output_dir, new_filename)
        
        # Process the image
        if process_image(input_file, output_file, config):
            # Create marker file to avoid reprocessing
            Path(marker_file).touch()

def main():
    """Main function to run the image processor."""
    args = parse_args()
    logger.info("Starting image processor")
    logger.info(f"Input directory: {args.input_dir}")
    logger.info(f"Output directory: {args.output_dir}")
    logger.info(f"Config file: {args.config_file}")
    logger.info(f"Sleep interval: {args.sleep_interval} seconds")
    
    if HEIC_SUPPORT:
        logger.info("HEIC format is supported")
    else:
        logger.warning("HEIC format is NOT supported")
    
    # Load configuration
    config = load_config(args.config_file)
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Main processing loop
    while True:
        process_files(args.input_dir, args.output_dir, config)
        logger.info(f"Sleeping for {args.sleep_interval} seconds...")
        time.sleep(args.sleep_interval)

if __name__ == "__main__":
    main()