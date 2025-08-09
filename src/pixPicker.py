import os
import cv2
import piexif
from PIL import Image
from moviepy.editor import VideoFileClip
from datetime import datetime
import subprocess

PHOTO_EXTS = (".jpg", ".jpeg", ".png", ".heic", ".heif")
VIDEO_EXTS = (".mp4", ".mov", ".avi", ".mkv")
TIME_GAP_THRESHOLD = 60 * 60  # 1 hour in seconds

FFMPEG_PATH = r"D:\projects\tools\ffmpeg-7.1.1-essentials_build\bin\ffmpeg.exe" 

def convert_heic_to_jpg(input_path, output_dir=None):
    """
    Convert HEIC to JPG using ffmpeg. 
    Returns path to JPG file.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(input_path)

    ext = os.path.splitext(input_path)[1].lower()
    if ext not in [".heic", ".heif"]:
        return input_path  # Already supported image type

    if output_dir is None:
        output_dir = os.path.dirname(input_path)

    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, os.path.splitext(os.path.basename(input_path))[0] + ".jpg")

    # Check if converted file already exists
    if os.path.exists(output_file):
        return output_file

    # ffmpeg command to convert HEIC to JPG
    cmd = [
        FFMPEG_PATH,
        "-y",  # overwrite
        "-i", input_path,
        output_file
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if result.returncode != 0:
        print(f"FFmpeg error for {input_path}: {result.stderr.decode()}")
        # Fall back to original file if conversion fails
        return input_path

    if not os.path.exists(output_file):
        print(f"Warning: HEIC conversion failed for {input_path}, using original")
        return input_path

    return output_file

def is_blurry(image_path, threshold=50):
    """Check if image is blurry using Laplacian variance."""
    try:
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if image is None:
            return True
        
        # Resize image for faster processing if it's very large
        height, width = image.shape
        if height > 1000 or width > 1000:
            scale = min(1000/height, 1000/width)
            new_height = int(height * scale)
            new_width = int(width * scale)
            image = cv2.resize(image, (new_width, new_height))
        
        variance = cv2.Laplacian(image, cv2.CV_64F).var()
        return variance < threshold
    except Exception as e:
        print(f"Warning: Could not check blur for {image_path}: {e}")
        return False  # Don't skip if we can't check

def get_photo_size_create_time(img_path):
    """Return (width, height, creation_time) for an image.
    Falls back to file modified time if creation time not available."""
    
    img_path = os.path.normpath(img_path)
    width, height = None, None
    creation_time = datetime.fromtimestamp(os.path.getmtime(img_path))
    
    try:
        img = Image.open(img_path)
        width, height = img.size
        
        # Try to get creation time from EXIF
        exif_bytes = img.info.get('exif')
        if exif_bytes:
            try:
                exif_dict = piexif.load(exif_bytes)
                
                # Try different EXIF fields for creation time
                datetime_str = exif_dict['Exif'].get(piexif.ExifIFD.DateTimeOriginal)
                if not datetime_str:
                    datetime_str = exif_dict['Exif'].get(piexif.ExifIFD.DateTime)
                if not datetime_str:
                    datetime_str = exif_dict['0th'].get(piexif.ImageIFD.DateTime)
                
                if datetime_str:
                    creation_time = datetime.strptime(datetime_str.decode(), "%Y:%m:%d %H:%M:%S")
                    
            except Exception as e:
                print(f"EXIF creation time parse failed for {img_path}: {e}")
                
    except Exception as e:
        print(f"Warning: Could not get size/creation time for {img_path}: {e}")
    
    return width, height, creation_time

def get_photo_metadata(image_path):
    """Return (timestamp, latitude, longitude) for an image.
    Falls back to file modified time and None for missing GPS."""
    
    image_path = os.path.normpath(image_path)    
    timestamp = datetime.fromtimestamp(os.path.getmtime(image_path))
    lat, lon = None, None

    try:
        img = Image.open(image_path)
        exif_bytes = img.info.get('exif')

        if exif_bytes:  # ✅ only load if EXIF exists
            try:
                exif_dict = piexif.load(exif_bytes)

                # --- Timestamp ---
                datetime_str = exif_dict['Exif'].get(piexif.ExifIFD.DateTimeOriginal)
                if datetime_str:
                    timestamp = datetime.strptime(datetime_str.decode(), "%Y:%m:%d %H:%M:%S")

                # --- GPS ---
                gps = exif_dict.get('GPS', {})

                def convert(coord):
                    """Convert GPS coordinate tuples to float degrees."""
                    if coord and all(isinstance(x, tuple) and x[1] != 0 for x in coord):
                        d, m, s = [x[0] / x[1] for x in coord]
                        return d + m / 60 + s / 3600
                    return None

                lat = convert(gps.get(piexif.GPSIFD.GPSLatitude))
                lon = convert(gps.get(piexif.GPSIFD.GPSLongitude))

                # GPSRef: South and West are negative
                lat_ref = gps.get(piexif.GPSIFD.GPSLatitudeRef)
                lon_ref = gps.get(piexif.GPSIFD.GPSLongitudeRef)
                if lat and lat_ref and lat_ref.decode() == 'S':
                    lat = -lat
                if lon and lon_ref and lon_ref.decode() == 'W':
                    lon = -lon

            except Exception as e:
                print(f"EXIF parse failed for {image_path}: {e}")

    except Exception as e:
        print(f"Warning: Could not read EXIF for {image_path}: {e}")

    return timestamp, lat, lon

def get_video_metadata(video_path):
    """Get video metadata with better error handling."""
    try:
        clip = VideoFileClip(video_path)
        timestamp = datetime.fromtimestamp(os.path.getmtime(video_path))
        duration = clip.duration
        width, height = clip.size
        clip.reader.close()
        clip.close()  # Ensure proper cleanup
        
        # More lenient criteria for video acceptance
        if duration < 1 or width < 50 or height < 50:
            return None  # skip very short or tiny videos
        return timestamp, duration
    except Exception as e:
        print(f"Warning: Could not get video metadata for {video_path}: {e}")
        return None

def get_one_media_item(folder, file):
    file_path = os.path.join(folder, file)        
    if file.startswith('.') or os.path.isdir(file_path):
        return None
            
    try:
        if file.lower().endswith(PHOTO_EXTS):
            original_file_path = file_path
            processing_path = file_path
            
            # Convert HEIC files if needed
            if file.lower().endswith((".heic", ".heif")):                                
                try:
                    processing_path = convert_heic_to_jpg(file_path)
                except Exception as e:
                    print(f"Warning: Could not convert HEIC file {file}: {e}")
                    return None
            
            # Check if image is blurry (skip if it is)
            if is_blurry(processing_path):
                print(f"Skipping blurry image: {file}")
                return None
                
            # Get metadata
            timestamp, lat, lon = get_photo_metadata(processing_path)
            width, height, creation_time = get_photo_size_create_time(processing_path)
            return {
                "type": "photo",
                "file": original_file_path,  # Keep original path for reference
                "converted_file": processing_path if processing_path != original_file_path else None,
                "timestamp": timestamp,
                "lat": lat,
                "lon": lon,
                "width": width,
                "height": height,
                "creation_time": creation_time
            }            
        elif file.lower().endswith(VIDEO_EXTS):
            meta = get_video_metadata(file_path)
            if meta:
                timestamp, duration = meta
                return {
                    "type": "video",
                    "file": file_path,
                    "timestamp": timestamp,
                    "duration": duration
                }                
    except Exception as e:
        print(f"Error processing {file}: {e}")    

def process_media(folder):
    """Process media files in a folder with improved error handling."""
    media_items = []
    files = os.listdir(folder)
    total_items = 0    
    for i, file in enumerate(files, 1):
        if total_items % 20 == 0:  # Progress update every 20 files
            print(f"Progress: {total_items} files processed")            
        file_path = os.path.join(folder, file)        
        if file.startswith('.') or os.path.isdir(file_path):
            continue
        media_item = get_one_media_item(folder, file)
        if media_item is not None:
            total_items += 1
            media_items.append(media_item)

    for i, flder in enumerate(files, 1):
        folder_path = os.path.join(folder, flder)
        if not os.path.isdir(folder_path):
            continue
        for j, file in enumerate(os.listdir(folder_path), 1):
            if (total_items > 0) and (total_items % 20 == 0):  # Progress update every 20 files
                print(f"Progress: {total_items} files processed")                 
            file_path = os.path.join(folder_path, file) 
            if file.startswith('.') or os.path.isdir(file_path):
                continue
            media_item = get_one_media_item(folder_path, file)
            if media_item is not None:
                total_items += 1
                media_items.append(media_item)

    print(f"Found {len(media_items)} valid media items")
    if media_items:
        media_items.sort(key=lambda x: x["timestamp"])
        return group_by_time(media_items)
    else:
        return []

def group_by_time(items):
    """Group items by time with proper handling of edge cases."""
    if not items:
        return []
    
    segments = []
    current = [items[0]]

    for prev, curr in zip(items, items[1:]):
        time_diff = (curr["timestamp"] - prev["timestamp"]).total_seconds()
        if time_diff > TIME_GAP_THRESHOLD:
            segments.append(current)
            current = []
        current.append(curr)
    
    if current:
        segments.append(current)
    
    return segments

# --- Run ---
if __name__ == "__main__":    
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    assets_input_dir = os.path.join(project_root, "assets", "input", "TableRocks_0726")
    
    print(f"Looking for media in: {assets_input_dir}")
    
    if not os.path.exists(assets_input_dir):
        print(f"Error: Assets input directory not found: {assets_input_dir}")
        exit(1)
    
    all_results = {}    
    print(f"\n=== Processing folder: {os.path.basename(assets_input_dir)} ===")
    try:
        segments = process_media(assets_input_dir)
        all_results[os.path.basename(assets_input_dir)] = segments
        
        # Show summary for this folder
        total_items = sum(len(segment) for segment in segments)
        print(f"Summary: {len(segments)} segments, {total_items} total items")
        
        # Show first few items as preview
        if segments:
            print("Preview of first segment:")
            for item in segments[0][:3]:  # Show first 3 items
                print(f"  {item['timestamp']} | {item['type'].upper()} | {os.path.basename(item['file'])}")
            if len(segments[0]) > 3:
                print(f"  ... and {len(segments[0]) - 3} more items")
                
    except Exception as e:
        print(f"Error processing {assets_input_dir}: {e}")
    
    # Final summary
    print(f"\n=== FINAL SUMMARY ===")
    total_segments = sum(len(segments) for segments in all_results.values())
    total_items = sum(sum(len(segment) for segment in segments) for segments in all_results.values())
    print(f"Processed {len(all_results)} folders")
    print(f"Total segments: {total_segments}")
    print(f"Total media items: {total_items}")
