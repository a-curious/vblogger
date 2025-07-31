import os
import cv2
import piexif
from PIL import Image
from moviepy.editor import VideoFileClip
from datetime import datetime

PHOTO_EXTS = (".jpg", ".jpeg", ".png")
VIDEO_EXTS = (".mp4", ".mov", ".avi", ".mkv")
TIME_GAP_THRESHOLD = 60 * 60  # 1 hour in seconds

def is_blurry(image_path, threshold=100):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        return True
    variance = cv2.Laplacian(image, cv2.CV_64F).var()
    return variance < threshold

def get_photo_metadata(image_path):
    try:
        img = Image.open(image_path)
        exif_dict = piexif.load(img.info.get('exif', b''))
        datetime_str = exif_dict['Exif'].get(piexif.ExifIFD.DateTimeOriginal)
        if datetime_str:
            timestamp = datetime.strptime(datetime_str.decode(), "%Y:%m:%d %H:%M:%S")
        else:
            timestamp = datetime.fromtimestamp(os.path.getmtime(image_path))

        gps = exif_dict.get('GPS', {})
        def convert(coord):
            if coord:
                d, m, s = [x[0] / x[1] for x in coord]
                return d + m / 60 + s / 3600
            return None
        lat = convert(gps.get(piexif.GPSIFD.GPSLatitude))
        lon = convert(gps.get(piexif.GPSIFD.GPSLongitude))
        return timestamp, lat, lon
    except:
        return datetime.fromtimestamp(os.path.getmtime(image_path)), None, None

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
    except:
        return None

def process_media(folder):
    media_items = []

    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)
        if file.lower().endswith(PHOTO_EXTS):
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
