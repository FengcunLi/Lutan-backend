import os
from random import randint

from django.conf import settings
from PIL import Image, ImageColor, ImageDraw, ImageFont

COLOR_WHEEL = (
    "#d32f2f",
    "#c2185b",
    "#7b1fa2",
    "#512da8",
    "#303f9f",
    "#1976d2",
    "#0288D1",
    "#0288d1",
    "#0097a7",
    "#00796b",
    "#388e3c",
    "#689f38",
    "#afb42b",
    "#fbc02d",
    "#ffa000",
    "#f57c00",
    "#e64a19",
)

FONT_FILE = os.path.join(os.path.dirname(__file__), "font.ttf")


def generate_default_avatar(char: str):
    avatar_size = max(settings.AVATARS_SIZES)
    image = Image.new("RGBA", (avatar_size, avatar_size), 0)
    image_size = image.size

    image_drawer = ImageDraw.Draw(image)

    # Draw background
    background_color = COLOR_WHEEL[randint(0, len(COLOR_WHEEL) - 1)]
    rgb = ImageColor.getrgb(background_color)
    image_drawer.rectangle([(0, 0), image_size], rgb)

    # draw singal character
    size = int(image_size[0] * 0.7)
    font = ImageFont.truetype(FONT_FILE, size=size)
    text_size = font.getsize(char)
    text_pos = ((image_size[0] - text_size[0]) / 2,
                (image_size[0] - text_size[1]) / 2)

    image_drawer.text(text_pos, char, font=font)

    return image
