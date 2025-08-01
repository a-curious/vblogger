import os
import cv2
import piexif
from PIL import Image
from moviepy.editor import VideoFileClip
from datetime import datetime
import subprocess

PHOTO_EXTS = (".jpg", ".jpeg", ".png") ### TODO, ".heic", ".heif")
VIDEO_EXTS = (".mp4", ".mov", ".avi", ".mkv")
TIME_GAP_THRESHOLD = 60 * 60  # 1 hour in seconds

FFMPEG_PATH = r"D:\projects\tools\ffmpeg-7.1.1-essentials_build\bin\ffmpeg.exe" 

# does not work
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

    # ffmpeg command to convert HEIC to JPG
    cmd = [
        FFMPEG_PATH,
        "-y",  # overwrite
        "-i", input_path,
        output_file
    ]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if not os.path.exists(output_file):
        raise RuntimeError(f"Failed to convert HEIC: {input_path}")

    return output_file


def is_blurry(image_path, threshold=100):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        return True
    variance = cv2.Laplacian(image, cv2.CV_64F).var()
    return variance < threshold

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
    try:
        clip = VideoFileClip(video_path)
        timestamp = datetime.fromtimestamp(os.path.getmtime(video_path))
        duration = clip.duration
        width, height = clip.size
        clip.reader.close()
        if duration < 2 or width < 100 or height < 100:
            return None  # skip blank videos
        return timestamp, duration
    except Exception as e:
        print(f"Warning: Could not get video meta data for {video_path}: {e}")
        return None

def process_media(folder):
    media_items = []

    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)
        if file.lower().endswith(PHOTO_EXTS):
            if file.lower().endswith((".heic", ".heif")):                                
                file_path = convert_heic_to_jpg(file_path)
            if is_blurry(file_path):
                continue
            timestamp, lat, lon = get_photo_metadata(file_path)
            media_items.append({
                "type": "photo",
                "file": file_path,
                "timestamp": timestamp,
                "lat": lat,
                "lon": lon
            })
        elif file.lower().endswith(VIDEO_EXTS):
            meta = get_video_metadata(file_path)
            if meta:
                timestamp, duration = meta
                media_items.append({
                    "type": "video",
                    "file": file_path,
                    "timestamp": timestamp,
                    "duration": duration
                })

    media_items.sort(key=lambda x: x["timestamp"])
    return group_by_time(media_items)

def group_by_time(items):
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
    folder = "D:\\projects\\AI_Projects\\vblog_creator\\code\\images"
    segments = process_media(folder)
    for i, segment in enumerate(segments):
        print(f"\n--- Segment {i+1} ---")
        for item in segment:
            print(f"{item['timestamp']} | {item['type'].upper()} | {item['file']}")
