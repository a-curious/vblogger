
FFPROBE_PATH  = r"D:\projects\tools\ffmpeg-7.1.1-essentials_build\bin\ffprobe.exe"  
TARGET_RATIO = 16/9

def fit_clip_to_size(clip, target_size=(1920,1080), bg_color=(0, 0, 0)):
    target_w, target_h = target_size
    clip_w, clip_h = clip.size

    scale = min(target_w / clip_w, target_h / clip_h)
    new_w = int(clip_w * scale)
    new_h = int(clip_h * scale)

    resized = clip.resize((new_w, new_h))

    padded = resized.on_color(
        size=target_size,
        color=bg_color,
        pos='center'
    )
    return padded