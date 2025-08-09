#!/usr/bin/env python3
"""
VBlogger - Video Blog Creator
Main entry point for the application.
"""

import sys
import os
import argparse

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.pixPicker import process_media
from src.composer import build_video
from config.config_loader import load_config, list_available_configs, validate_config


def main():
    """Main function to run the video creation process."""
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='VBlogger - Video Blog Creator')
    parser.add_argument('--config', '-c', 
                       default='table_rocks_config',
                       help='Configuration file name (without .py extension)')
    parser.add_argument('--list-configs', '-l', 
                       action='store_true',
                       help='List available configurations')
    parser.add_argument('--testing', '-t', 
                       action='store_true',
                       help='Run in testing mode')
    
    args = parser.parse_args()
    
    # List available configs if requested
    if args.list_configs:
        try:
            configs = list_available_configs()
            print("Available configurations:")
            for config in configs:
                print(f"  - {config}")
        except Exception as e:
            print(f"Error listing configs: {e}")
            import traceback
            traceback.print_exc()
        return
    
    try:
        # Load configuration
        if args.testing:
            print(f"Overriding configuration from {args.config} to temp_config")
            config = load_config("temp_config")
            config['TESTING_MODE'] = True
            print("Running in testing mode")
        else:
            print(f"Loading configuration from {args.config}")
            config = load_config(args.config)
        
        # Validate configuration
        validate_config(config)
        
        
        # Extract parameters from config
        folder = config['INPUT_FOLDER']
        title = config['TITLE']
        subtitle = config['SUBTITLE']
        final_file = config['OUTPUT_FILE']
        music = config['MUSIC_FILE']
        
        # Use testing folder if in testing mode
        if config['TESTING_MODE']:
            folder = r"assets\input\temp"
            final_file = r"assets\output\test.mp4"
            print(f"Testing mode: using {folder}")
        
        print(f"Processing folder: {folder}")
        print(f"Output file: {final_file}")
        print(f"Title: {title}")
        print(f"Subtitle: {subtitle}")
        print(f"Music: {music}")
        
        # Process media
        segments = process_media(folder)
        totalCnt = 1
        for i, segment in enumerate(segments):
            print(f"\n--- Segment {i+1} ---")
            for item in segment:            
                print(f"{item['timestamp']} | {item['type'].upper()} | {item['file']}")
                totalCnt += 1
        print(f"\n--- {totalCnt} ---")

        # Build video
        build_video(segments, final_file, title, subtitle, music)
        
        print(f"\n✅ Video created successfully: {final_file}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 