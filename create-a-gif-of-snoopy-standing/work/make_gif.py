from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math

W = H = 640
OUT = Path(__file__).parents[1] / "outputs" / "snoopy_please_stay_love.gif"
OUT.parent.mkdir(parents=True, exist_ok=True)

INK = (45, 42, 38)
PAPER = (255, 252, 243)
BG = (250, 241, 224)
BLUE = (201, 221, 226)
BLUSH = (239, 205, 199)

font_path = "C:/Windows/Fonts/segoepr.ttf"
font = ImageFont.truetype(font_path, 37)
small_font = ImageFont.truetype(font_path, 28)

def line(draw, points, width=5, fill=INK):
    draw.line(points, fill=fill, width=width, joint="curve")

def frame(t):
    # t moves from 0 to 1 as the sign is gently raised.
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    # barely-there nostalgic sun wash / ground shadow
    d.ellipse((125, 77, 515, 467), fill=(251, 237, 214))
    d.ellipse((185, 550, 455, 581), fill=(224, 211, 191))

    bob = math.sin(t * math.pi) * 4
    # upright white beagle body
    d.ellipse((248, 292 + bob, 396, 540 + bob), fill=PAPER, outline=INK, width=6)
    # little tail
    d.arc((370, 386 + bob, 458, 455 + bob), 245, 72, fill=INK, width=6)
    line(d, [(390, 428 + bob), (430, 420 + bob), (444, 442 + bob)], 6)
    # feet
    d.ellipse((230, 520 + bob, 306, 556 + bob), fill=PAPER, outline=INK, width=5)
    d.ellipse((341, 520 + bob, 417, 556 + bob), fill=PAPER, outline=INK, width=5)

    # large soft rounded head
    d.ellipse((202, 145 + bob, 442, 358 + bob), fill=PAPER, outline=INK, width=6)
    # long floppy ears
    d.ellipse((184, 164 + bob, 250, 329 + bob), fill=INK)
    d.ellipse((392, 165 + bob, 450, 307 + bob), fill=INK)
    # muzzle and simple tender face
    d.ellipse((285, 232 + bob, 397, 321 + bob), fill=PAPER, outline=INK, width=4)
    d.ellipse((326, 246 + bob, 348, 265 + bob), fill=INK)
    d.ellipse((304, 219 + bob, 316, 232 + bob), fill=INK)
    d.arc((324, 264 + bob, 366, 301 + bob), 5, 165, fill=INK, width=4)
    # rosy cheeks
    d.ellipse((275, 275 + bob, 299, 287 + bob), fill=BLUSH)
    d.ellipse((367, 275 + bob, 391, 287 + bob), fill=BLUSH)
    # collar
    d.arc((255, 330 + bob, 391, 367 + bob), 0, 180, fill=(173, 188, 196), width=9)

    # sign travels from below the scene to chest height.
    sy = int(605 - 235 * t)
    sx, sw, sh = 150, 340, 116
    # arms appear to bring it forward
    ly = int(430 - 108 * t + bob)
    ry = int(430 - 108 * t + bob)
    line(d, [(268, 392 + bob), (239, ly), (sx + 31, sy + 62)], 8)
    line(d, [(375, 392 + bob), (405, ry), (sx + sw - 30, sy + 62)], 8)
    d.ellipse((sx + 17, sy + 49, sx + 50, sy + 80), fill=PAPER, outline=INK, width=4)
    d.ellipse((sx + sw - 50, sy + 49, sx + sw - 17, sy + 80), fill=PAPER, outline=INK, width=4)
    # paper sign (with friendly irregular outline)
    polygon = [(sx, sy + 6), (sx + sw - 2, sy), (sx + sw, sy + sh - 5), (sx + 5, sy + sh)]
    d.polygon(polygon, fill=(255, 253, 247))
    line(d, polygon + [polygon[0]], 5)
    # extremely legible exact line of text
    message = "please stay, Love"
    bbox = d.textbbox((0, 0), message, font=font)
    tx = sx + (sw - (bbox[2] - bbox[0])) // 2
    d.text((tx, sy + 36), message, font=font, fill=INK, stroke_width=0)
    # tiny warm heart, not text
    hx, hy = sx + sw - 29, sy + 23
    d.polygon([(hx,hy+5),(hx-9,hy-5),(hx-16,hy+5),(hx,hy+20),(hx+16,hy+5),(hx+9,hy-5)], fill=BLUSH)
    return im

# Gentle reveal: five short raising frames, then a long reading hold with subtle bobbing.
progress = [0, .16, .34, .55, .77, 1.0] + [1.0] * 12
frames = [frame(p) for p in progress]
durations = [120, 120, 120, 120, 160, 300] + [330] * 12
frames[0].save(OUT, save_all=True, append_images=frames[1:], duration=durations, loop=0, disposal=2)
print(OUT)
