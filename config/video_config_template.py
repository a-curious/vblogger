"""
Video Configuration Template
Copy this file and rename it for each video project.
Example: table_rocks_config.py, wuhan_trip_config.py
"""

# Input/Output Paths
INPUT_FOLDER = r"assets\input\images"  # Path to input images/videos
OUTPUT_FILE = r"assets\output\Table_Rocks_20250726.mp4"  # Output video filename
MUSIC_FILE = r"assets\music\Summer.m4a"  # Background music file

# Video Content
TITLE = "Table Rocks Lost City"  # Main title
SUBTITLE = "July 26, 2025"  # Subtitle

# Visual Settings
FILL_COLOR = "(0, 128, 128, 255)"  # Background color (RGBA)
TEXT_COLOR = "white"  # Text color
TEXT_STROKE_COLOR = "black"  # Text outline color
TEXT_STROKE_WIDTH = 2  # Text outline width

# Timing Settings
PHOTO_DURATION = 3.0  # Duration for each photo (seconds)
VIDEO_DURATION = 5.0  # Duration for each video (seconds)
TRANSITION_DURATION = 0.5  # Transition duration (seconds)
COVER_DURATION = 3.0  # Title/ending screen duration (seconds)

# Video Quality
VIDEO_WIDTH = 1920  # Output video width
VIDEO_HEIGHT = 1080  # Output video height
FPS = 30  # Frames per second

# Audio Settings
MUSIC_VOLUME = 0.2  # Background music volume (0.0 to 1.0)
AUDIO_FADE_IN = 1.0  # Music fade in duration (seconds)
AUDIO_FADE_OUT = 2.0  # Music fade out duration (seconds)

# Processing Options
TESTING_MODE = False  # Set to True for testing with fewer files
AUTO_ASPECT_RATIO = True  # Automatically handle aspect ratio issues 