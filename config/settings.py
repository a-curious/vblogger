"""
Configuration settings for VBlogger
"""

import os

# Project paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(PROJECT_ROOT, "assets")
INPUT_DIR = os.path.join(ASSETS_DIR, "input")
OUTPUT_DIR = os.path.join(ASSETS_DIR, "output")
MUSIC_DIR = os.path.join(ASSETS_DIR, "music")

# Default settings
DEFAULT_PHOTO_DURATION = 3.0  # seconds
DEFAULT_VIDEO_DURATION = 5.0  # seconds
DEFAULT_TRANSITION_DURATION = 0.5  # seconds

# Video settings
DEFAULT_VIDEO_WIDTH = 1920
DEFAULT_VIDEO_HEIGHT = 1080
DEFAULT_FPS = 30

# Audio settings
DEFAULT_AUDIO_FADE_IN = 1.0  # seconds
DEFAULT_AUDIO_FADE_OUT = 2.0  # seconds

# Text settings
DEFAULT_TITLE_FONT_SIZE = 60
DEFAULT_SUBTITLE_FONT_SIZE = 40
DEFAULT_TEXT_COLOR = "white"
DEFAULT_TEXT_STROKE_COLOR = "black"
DEFAULT_TEXT_STROKE_WIDTH = 2

# File extensions
SUPPORTED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.heic', '.heif']
SUPPORTED_VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv']
SUPPORTED_AUDIO_EXTENSIONS = ['.mp3', '.wav', '.m4a', '.aac', '.flac'] 