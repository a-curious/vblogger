import os
from datetime import datetime
import mimetypes
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, Dict, Any

import exifread
from PIL import Image
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
import subprocess
import json

PHOTO_EXTS = (".jpg", ".jpeg", ".png", ".heic", ".heif")
VIDEO_EXTS = (".mp4", ".mov", ".avi", ".mkv")

@dataclass
class GeneralMetadata:
    filename: str
    filepath: str
    size_bytes: int
    created_time: str
    modified_time: str
    mime_type: str

@dataclass
class ImageMetadata:
    format: Optional[str] = None
    mode: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    exif_data: Dict[str, Any] = field(default_factory=dict)

@dataclass
class VideoMetadata:
    duration: Optional[float] = None
    codec: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    frame_rate: Optional[float] = None
    bit_rate: Optional[int] = None
    audio_codec: Optional[str] = None
    other_metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MediaMetadata:
    general: GeneralMetadata
    image: Optional[ImageMetadata] = None
    video: Optional[VideoMetadata] = None


def get_general_metadata(path: Path) -> GeneralMetadata:
    stat = path.stat()
    mime_type, _ = mimetypes.guess_type(path)

    def format_time(ts):
        return datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    return GeneralMetadata(
        filename=path.name,
        filepath=str(path.resolve()),
        size_bytes=stat.st_size,
        created_time=format_time(stat.st_ctime),
        modified_time=format_time(stat.st_mtime),
        mime_type=mime_type or "unknown"
    )

def get_image_metadata(path: Path) -> ImageMetadata:
    metadata = ImageMetadata()
    try:
        with Image.open(path) as img:
            metadata.format = img.format
            metadata.mode = img.mode
            metadata.width, metadata.height = img.size

        with open(path, 'rb') as f:
            exif_tags = exifread.process_file(f, details=False)
            metadata.exif_data = {k: str(v) for k, v in exif_tags.items()}
    except Exception as e:
        print(f"Error reading image metadata: {e}")
    return metadata

def get_video_metadata(path: Path) -> VideoMetadata:
    metadata = VideoMetadata()

    try:
        # Use ffprobe to get detailed metadata
        cmd = [
            "ffprobe",
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            str(path)
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            data = json.loads(result.stdout)

            for stream in data.get('streams', []):
                if stream['codec_type'] == 'video':
                    metadata.codec = stream.get('codec_name')
                    metadata.width = stream.get('width')
                    metadata.height = stream.get('height')
                    metadata.frame_rate = eval(stream.get('r_frame_rate', '0'))
                    metadata.bit_rate = int(stream.get('bit_rate', 0))
                elif stream['codec_type'] == 'audio':
                    metadata.audio_codec = stream.get('codec_name')

            fmt = data.get("format", {})
            metadata.duration = float(fmt.get('duration', 0))
            metadata.other_metadata = fmt
    except Exception as e:
        print(f"Error reading video metadata: {e}")
    return metadata


def get_meta_data(file_path: str) -> MediaMetadata:
    path = Path(file_path)
    general_meta = get_general_metadata(path)

    if general_meta.mime_type:
        if general_meta.mime_type.startswith("image"):
            image_meta = get_image_metadata(path)
            return MediaMetadata(general=general_meta, image=image_meta)
        elif general_meta.mime_type.startswith("video"):
            video_meta = get_video_metadata(path)
            return MediaMetadata(general=general_meta, video=video_meta)

    # fallback: try both
    image_meta = get_image_metadata(path)
    video_meta = get_video_metadata(path)
    return MediaMetadata(general=general_meta, image=image_meta, video=video_meta)

if __name__ == "__main__":
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    assets_input_dir = os.path.join(project_root, "assets", "input", "TableRocks_0726")
    
    print(f"Looking for media in: {assets_input_dir}")
    
    if not os.path.exists(assets_input_dir):
        print(f"Error: Assets input directory not found: {assets_input_dir}")
        exit(1)
    
    media_items = []
    files = os.listdir(assets_input_dir)
    total_files = len(files)
    
    print(f"Processing {total_files} files...")    
    for i, file in enumerate(files, 1):
        if i % 20 == 0:  # Progress update every 20 files
            print(f"Progress: {i}/{total_files} files processed")
            
        file_path = os.path.join(assets_input_dir, file)
        
        # Skip hidden files and directories
        if file.startswith('.') or os.path.isdir(file_path):
            continue
            
        try:
            if file.lower().endswith(PHOTO_EXTS):
                original_file_path = file_path
                processing_path = file_path
                meta = get_meta_data(file_path)
                print(meta)
                media_items.append(meta)
            elif file.lower().endswith(VIDEO_EXTS):
                meta = get_meta_data(file_path)
                media_items.append(meta)
        except Exception as e:
            print(f"Error processing {file}: {e}")
            continue
        
    print(f"Total media items: {media_items}")
   
   