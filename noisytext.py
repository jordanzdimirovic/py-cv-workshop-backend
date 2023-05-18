"""
A script that generates text (with different fonts) on a "Gaussian" noisy background.
"""

from argparse import ArgumentParser
import io
import math
import random
from PIL import Image, ImageDraw, ImageFont
import numpy as np

GAUSS_MEAN = 0
GAUSS_VARIANCE = 0.1
GAUSS_SIGMA = math.sqrt(GAUSS_VARIANCE)

FONT_CHOICES = "calibril.ttf arial.ttf times.ttf".split(' ')

def generate_text_on_gaussian(text: str, width: int = 800, height: int = 400) -> io.BytesIO:
    # Create blank
    img = Image.new('L', (width, height), color='white')

    # Generate noisy background
    noise = np.random.normal(GAUSS_MEAN, GAUSS_SIGMA, (height, width))
    noise_img = Image.fromarray((noise * 255).astype(np.uint8))

    # Write text on the image
    draw = ImageDraw.Draw(noise_img)
    # font_size = int(0.5 * (width + height) // len(text))
    font_size = int(1.9 * width // len(text))
    font = ImageFont.truetype(random.choice(FONT_CHOICES), font_size)

    v = draw.textbbox((0,0), text, font)
    text_w = v[2] - v[0]
    text_h = v[3] - v[1]
    x, y = (width - text_w) // 2, (height - text_h) // 2

    draw.text((x, y - text_h // 4), text, font=font, fill=0)

    res = io.BytesIO()

    noise_img.save(res, format="JPEG")
    
    return res



if __name__ == "__main__":
    ap = ArgumentParser(description="Generates text on Gaussian noise")
    ap.add_argument("text", type=str)
    ap.add_argument("-x", default=400, type=int)
    ap.add_argument("-y", default=300, type=int)
    ap.add_argument("-o", type=str, required=True)

    args = ap.parse_args()

    jpg_bytes = generate_text_on_gaussian(
        args.text,
        args.x,
        args.y
    )

    with open(args.o, "wb") as f:
        f.write(jpg_bytes.getvalue())
    
