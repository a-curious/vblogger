import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'utils'))
from formatHelper import filename_to_subtitle, create_subtitled_clip, PHOTO_DURATION, create_cover_clip
from handleAspectRatio import pad_video, resize_and_pad, if_need_padding
from moviepy.audio.fx.all import audio_loop
from moviepy.editor import (
    VideoFileClip, 
    ImageClip, 
    concatenate_videoclips, 
    # TextClip, 
    # CompositeVideoClip, 
    CompositeAudioClip,
    AudioFileClip
)

def create_media_clips(segments):
    media_clips = []
    for i, segment in enumerate(segments):
        # print(f"\n--- Adding {i+1} ---")
        for item in segment:
            vfile = item['file']
            fname = os.path.basename(vfile)
            subtitle = filename_to_subtitle(fname)
            if item['type'] == "photo":
                clip = ImageClip(vfile).set_duration(PHOTO_DURATION)
                clip = resize_and_pad(clip)                
                clip = create_subtitled_clip(clip, subtitle, PHOTO_DURATION)
            elif item['type'] == "video":
                clip = VideoFileClip(vfile)
                needPad = if_need_padding(vfile)
                if (needPad):                    
                    print("--- Padding {vfile} ---")
                    correct_width = int(clip.h * 9 / 16)  # DAR 9:16
                    clip = clip.resize(newsize=(correct_width, clip.h))              
                    clip = pad_video(clip)                
                clip = create_subtitled_clip(clip, subtitle, clip.duration)
            media_clips.append(clip)
    return media_clips


# --- Create final video ---
def build_video(segments, output_file, title, subtitle, music_file=None):
    clips = create_media_clips(segments)
    cover = create_cover_clip(title=title, subtitle=subtitle, duration=3 )  # seconds
    
    back_cover = create_cover_clip(
       title="Welcome back!",
        subtitle="See you soon",
        duration=3  # seconds
    )

    final_clip = concatenate_videoclips([cover] + clips + [back_cover], method="compose")

    if music_file and os.path.exists(music_file):
        # Use fps=44100 and buffersize to limit memory usage
        audio = AudioFileClip(music_file, fps=44100, buffersize=20000).volumex(0.2)
        video_duration = final_clip.duration
        audio_looped = audio_loop(audio, duration=video_duration)

        # Mix with original video audio
        mixed_audio = CompositeAudioClip([final_clip.audio, audio_looped])
        final = final_clip.set_audio(mixed_audio)

    final.write_videofile(output_file, codec="libx264", audio_codec="aac", threads=4, ffmpeg_params=["-movflags", "faststart"])


# --- Run it ---
if __name__ == "__main__":
    SEGMENT = [  # Replace with your actual segment list
        {"type": "photo", "file": "media/photo1.jpg"},
        {"type": "video", "file": "media/video1.mp4"},
        {"type": "photo", "file": "media/photo2.jpg"},
    ]
    OUTPUT_FILE = "final_video.mp4"
    BACKGROUND_MUSIC = "audio/music.mp3"  # Can be royalty-free
    VIDEO_RES = (1280, 720)
    PHOTO_DURATION = 4  # seconds per photo
    FONT = "Arial-Bold"

    # Example subtitle per media item
    subtitles = {
        "photo1.jpg": "Starting the hike early morning",
        "video1.mp4": "Reaching the viewpoint",
        "photo2.jpg": "Final stretch before summit"
    }

    build_video(SEGMENT, OUTPUT_FILE, BACKGROUND_MUSIC)
