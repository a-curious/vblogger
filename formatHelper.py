import os
import re
from PIL import Image, ImageDraw, ImageFont
import tempfile
from moviepy.editor import ImageClip, CompositeVideoClip

def filename_to_subtitle(filename):
    base = os.path.splitext(os.path.basename(filename))[0]

    # Replace underscores and dashes with spaces
    base = re.sub(r"[_\-]", " ", base)

    # Add space before capital letters (CamelCase → Camel Case)
    base = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", base)

    # Capitalize each word
    return base.title()

PHOTO_DURATION = 3  # seconds per photo
FONT = "Arial-Bold"

def generate_subtitle_image(text, size=(1280, 100), font_size=40):
    img = Image.new("RGBA", size, (0, 0, 0, 128))  # semi-transparent black box
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    # Use textbbox instead of deprecated textsize
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    position = ((size[0] - text_width) // 2, (size[1] - text_height) // 2)
    draw.text(position, text, font=font, fill=(255, 255, 255, 255))

    temp_path = tempfile.mktemp(suffix=".png")
    img.save(temp_path)
    return temp_path

def create_subtitled_clip(clip, subtitle_text, duration) -> CompositeVideoClip:
    subtitle_img_path = generate_subtitle_image(subtitle_text)
    subtitle_img = ImageClip(subtitle_img_path).set_duration(duration).set_position(("center", "bottom"))
    return CompositeVideoClip([clip, subtitle_img])

def generate_title_image(title, subtitle, size=(1280, 720), title_size=80, subtitle_size=50):
    img = Image.new("RGBA", size, (0, 128, 128, 255))  # solid teal background
    draw = ImageDraw.Draw(img)

    try:
        title_font = ImageFont.truetype("arial.ttf", title_size)
        subtitle_font = ImageFont.truetype("arial.ttf", subtitle_size)
    except IOError:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()

    # Title
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_position = ((size[0] - title_width) // 2, size[1] // 2 - 80)

    # Subtitle
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_position = ((size[0] - subtitle_width) // 2, size[1] // 2 + 20)

    draw.text(title_position, title, font=title_font, fill=(255, 255, 255, 255))
    draw.text(subtitle_position, subtitle, font=subtitle_font, fill=(180, 180, 180, 255))

    temp_path = tempfile.mktemp(suffix=".png")
    img.save(temp_path)
    return temp_path


def create_cover_clip(title, subtitle, duration=4, size=(1280, 720)):
    image_path = generate_title_image(title, subtitle, size=size)
    clip = ImageClip(image_path).set_duration(duration)
    return clip

