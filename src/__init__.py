"""
VBlogger - Video Blog Creator
A Python package for creating video blogs from images and videos.
"""

__version__ = "1.0.0"
__author__ = "VBlogger Team"

from .pixPicker import process_media
from .composer import build_video

__all__ = ['process_media', 'build_video'] 