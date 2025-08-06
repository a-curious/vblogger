#!/usr/bin/env python3
"""
Configuration Creator
Helper script to create new video configurations.
"""

import sys
import os
from config.config_loader import create_config_from_template, list_available_configs


def main():
    """Interactive configuration creator."""
    
    print("🎬 VBlogger Configuration Creator")
    print("=" * 40)
    
    # List existing configs
    existing_configs = list_available_configs()
    if existing_configs:
        print(f"Existing configurations: {', '.join(existing_configs)}")
    print()
    
    # Get new config name
    config_name = input("Enter name for new configuration (e.g., 'my_vacation_config'): ").strip()
    if not config_name:
        print("❌ Configuration name is required")
        return
    
    if not config_name.endswith('_config'):
        config_name += '_config'
    
    # Check if config already exists
    config_file = os.path.join('config', f"{config_name}.py")
    if os.path.exists(config_file):
        overwrite = input(f"Configuration '{config_name}' already exists. Overwrite? (y/N): ").strip().lower()
        if overwrite != 'y':
            print("❌ Cancelled")
            return
    
    print(f"\nCreating configuration: {config_name}")
    print("Enter the following parameters (press Enter to use defaults):")
    
    # Get parameters
    params = {}
    
    # Required parameters
    params['INPUT_FOLDER'] = input("Input folder path (default: assets/input/images): ").strip() or r"assets\input\images"
    params['OUTPUT_FILE'] = input("Output video filename (default: assets/output/my_video.mp4): ").strip() or r"assets\output\my_video.mp4"
    params['MUSIC_FILE'] = input("Music file path (default: assets/music/Summer.m4a): ").strip() or r"assets\music\Summer.m4a"
    params['TITLE'] = input("Video title: ").strip() or "My Video"
    params['SUBTITLE'] = input("Video subtitle: ").strip() or "Created with VBlogger"
    
    # Optional parameters
    fill_color = input("Background color RGBA (default: (0, 128, 128, 255)): ").strip()
    if fill_color:
        params['FILL_COLOR'] = fill_color
    
    photo_duration = input("Photo duration in seconds (default: 3.0): ").strip()
    if photo_duration:
        try:
            params['PHOTO_DURATION'] = float(photo_duration)
        except ValueError:
            print("⚠️  Invalid photo duration, using default")
    
    video_duration = input("Video duration in seconds (default: 5.0): ").strip()
    if video_duration:
        try:
            params['VIDEO_DURATION'] = float(video_duration)
        except ValueError:
            print("⚠️  Invalid video duration, using default")
    
    # Create the configuration
    try:
        config_path = create_config_from_template('video_config_template', config_name, **params)
        print(f"\n✅ Configuration created: {config_path}")
        print(f"\nTo use this configuration, run:")
        print(f"python vblogger_main.py --config {config_name}")
        
    except Exception as e:
        print(f"❌ Error creating configuration: {e}")


if __name__ == "__main__":
    main() 