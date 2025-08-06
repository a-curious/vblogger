import os, subprocess, json
from moviepy.editor import VideoFileClip, CompositeVideoClip, ColorClip

FFPROBE_PATH  = r"D:\projects\tools\ffmpeg-7.1.1-essentials_build\bin\ffprobe.exe"  
TARGET_RATIO = 16/9

def if_need_padding(video_file, threshold=0.05):
    print(f"\n--- Checking {video_file} ---")
    if not os.path.exists(video_file):
        raise FileNotFoundError(video_file)
    
    if "__" in video_file:
        return False
    
    cmd = [
        FFPROBE_PATH ,
        "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height,sample_aspect_ratio",
        "-of", "json",
        video_file
    ]

    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    info = json.loads(result.stdout)

    stream = info["streams"][0]
    width = stream["width"]
    height = stream["height"]

    # Handle sample_aspect_ratio (SAR)
    sar = stream.get("sample_aspect_ratio", "1:1")
    sar_w, sar_h = map(int, sar.split(":"))
    real_dar = (width * sar_w) / (height * sar_h)  # Display Aspect Ratio

    # Decide if needs padding
    if abs(real_dar - TARGET_RATIO) <= threshold:
        return True
    else:
        return False

def pad_video(clip, final_size=(1920, 1080), color=(0, 128, 128)):
    """
    Pad the video to final_size with solid color without stretching.
    Keeps the original video as-is.
    """
    # Create a solid background
    bg = (VideoFileClip(clip.filename)
          .resize(height=1)  # Hack to get duration without loading frames
          .set_duration(clip.duration)
          .fx(lambda c: c)  # no-op
         )
    bg = bg.on_color(
        size=final_size,
        color=color,
        pos='center',
        col_opacity=1
    )
    
    # Overlay original video centered
    padded = CompositeVideoClip([clip.set_position('center')], size=final_size)
    padded = padded.set_duration(clip.duration)
    return padded

def fix_aspect_ratio(clip, target_ratio=9/16):
    # Only fix if current ratio is suspiciously narrow or wide
    current_ratio = clip.w / clip.h
    if abs(current_ratio - target_ratio) > 0.1:
        new_width = int(clip.h * target_ratio)
        print(f"Fixing aspect ratio: {clip.w}x{clip.h} → {new_width}x{clip.h}")
        return clip.resize(width=new_width)
    return clip

# target_size=(1280, 720), bg_color=(0, 0, 0)
# 1920，1080
# 2276, 1280
def resize_and_pad(clip, target_size=(1280, 720), bg_color=(0, 128, 128)):
    print(f"Original size: {clip.size}")  # [width, height]
    # clip = fix_aspect_ratio(clip)
    # print(f"Fixed size: {clip.size}")  # [width, height]

    clip = clip.resize(height=target_size[1], width=target_size[0])

    # # # Resize to fit height or width while preserving aspect ratio
    # clip = clip.resize(height=target_size[1]) if clip.h < target_size[1] else clip.resize(width=target_size[0])
    
    # Make a background clip of the target size    
    background = ColorClip(size=target_size, color=bg_color).set_duration(clip.duration)

    # Center the resized clip over the background
    composite = CompositeVideoClip([background, clip.set_position("center")])
    return composite.set_duration(clip.duration)



# INPUT_FOLDER = "input_videos"
# OUTPUT_FOLDER = "fixed_videos"

# def get_video_info(filepath):
#     cmd = [
#         "ffprobe", "-v", "error", "-select_streams", "v:0",
#         "-show_entries", "stream=width,height,display_aspect_ratio",
#         "-of", "json", filepath
#     ]
#     output = subprocess.check_output(cmd)
#     data = json.loads(output)
#     return data['streams'][0]

# def should_fix(width, height, dar):
#     if not dar or ':' not in dar:
#         return False

#     dar_w, dar_h = map(int, dar.split(':'))
#     target_ratio = dar_w / dar_h
#     actual_ratio = width / height

#     return abs(actual_ratio - target_ratio) > 0.05

# def fix_video(filepath, output_path, target_dar):
#     width, height = get_target_resolution(filepath, target_dar)
#     print(f" → Fixing to {width}x{height} DAR={target_dar}")
    
#     cmd = [
#         "ffmpeg", "-y", "-i", filepath,
#         "-vf", f"scale={width}:{height},setdar={target_dar}",
#         "-c:a", "copy",
#         output_path
#     ]
#     subprocess.run(cmd)

# def get_target_resolution(filepath, target_dar):
#     info = get_video_info(filepath)
#     height = info['height']
#     dar_w, dar_h = map(int, target_dar.split(':'))
#     target_width = int(height * (dar_w / dar_h))
#     return target_width, height

# def main():
#     os.makedirs(OUTPUT_FOLDER, exist_ok=True)

#     for filename in os.listdir(INPUT_FOLDER):
#         if not filename.lower().endswith((".mp4", ".mov", ".mkv")):
#             continue

#         input_path = os.path.join(INPUT_FOLDER, filename)
#         output_path = os.path.join(OUTPUT_FOLDER, filename)

#         try:
#             info = get_video_info(input_path)
#             width = info['width']
#             height = info['height']
#             dar = info.get('display_aspect_ratio', '')

#             print(f"Checking {filename}: {width}x{height}, DAR={dar}")
#             if should_fix(width, height, dar):
#                 fix_video(input_path, output_path, dar)
#             else:
#                 print(" → Skipped (aspect ratio OK)")
#         except Exception as e:
#             print(f"Error processing")
