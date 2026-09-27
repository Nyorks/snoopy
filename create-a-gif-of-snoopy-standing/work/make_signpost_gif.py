from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math

W, H = 640, 700
OUT = Path(__file__).parents[1] / "outputs" / "snoopy_signpost_please_stay_love.gif"
INK, BG, PAPER = (43, 40, 37), (244, 241, 235), (255, 253, 247)
YELLOW, RED, SHADOW = (248, 197, 47), (211, 73, 64), (207, 202, 192)
FONT = ImageFont.truetype("C:/Windows/Fonts/segoepr.ttf", 43)

def stroke(draw, xy, width=5, fill=INK):
    draw.line(xy, fill=fill, width=width, joint="curve")

def make_frame(reveal, blink=False):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    # Ground shadow and signpost.
    d.ellipse((111, 625, 511, 660), fill=SHADOW)
    d.rectangle((305, 66, 335, 510), fill=(156, 125, 82), outline=INK, width=4)
    for x in (312, 321, 329): stroke(d, [(x, 70), (x-3, 505)], 2, (105, 81, 55))
    # Sign drops gently into its final position.
    top = int(-110 + 170 * reveal)
    bottom = top + 245
    left, right = 79, 558
    poly = [(left+8, top+9), (right-7, top+1), (right, bottom-7), (right-13, bottom), (left+11, bottom-2), (left, bottom-16), (left+4, top+22)]
    d.polygon(poly, fill=PAPER)
    stroke(d, poly + [poly[0]], 5)
    # perfectly readable sign text, revealed after board arrives
    if reveal > .68:
        message = "please stay, Love"
        box = d.textbbox((0, 0), message, font=FONT)
        tx = (W - (box[2]-box[0])) // 2
        shade = int(43 + (1-reveal) * 190)
        d.text((tx, top + 102), message, font=FONT, fill=(shade, shade-3, shade-6))
    # seated white beagle
    bob = 2 if reveal < .45 else 0
    # body, paws, tail
    d.ellipse((238, 452+bob, 415, 624+bob), fill=PAPER, outline=INK, width=6)
    d.ellipse((218, 577+bob, 292, 641+bob), fill=PAPER, outline=INK, width=5)
    d.ellipse((350, 577+bob, 423, 641+bob), fill=PAPER, outline=INK, width=5)
    stroke(d, [(405, 560+bob), (450, 579+bob), (434, 600+bob)], 5)
    # Snoopy-inspired side-profile head: long rounded snout, floppy ear, and small dot eyes.
    d.ellipse((178, 370+bob, 405, 536+bob), fill=PAPER)
    d.ellipse((315, 402+bob, 475, 502+bob), fill=PAPER)
    d.arc((178, 370+bob, 405, 536+bob), 88, 282, fill=INK, width=6)
    d.arc((315, 402+bob, 475, 502+bob), 260, 90, fill=INK, width=6)
    stroke(d, [(255, 374+bob), (312, 371+bob), (366, 386+bob), (404, 413+bob)], 6)
    # floppy black ear, tucked behind the left side of the face
    d.ellipse((171, 382+bob, 238, 526+bob), fill=INK)
    # yellow cap, brim and crown
    d.ellipse((220, 335+bob, 392, 406+bob), fill=YELLOW, outline=INK, width=5)
    d.pieslice((285, 307+bob, 418, 414+bob), 195, 40, fill=YELLOW, outline=INK, width=5)
    stroke(d, [(304, 345+bob), (350, 363+bob), (385, 390+bob)], 3, (173, 126, 26))
    # face
    if blink:
        stroke(d, [(306, 433+bob), (320, 433+bob)], 4)
        stroke(d, [(338, 438+bob), (352, 438+bob)], 4)
    else:
        d.ellipse((307, 423+bob, 319, 438+bob), fill=INK)
        d.ellipse((340, 427+bob, 352, 442+bob), fill=INK)
    # small rounded nose at the end of the profile snout, and a gentle smile below it
    d.ellipse((430, 442+bob, 457, 460+bob), fill=INK)
    d.arc((336, 452+bob, 412, 498+bob), 20, 158, fill=INK, width=4)
    # red collar, tag
    d.arc((255, 520+bob, 390, 557+bob), 0, 180, fill=RED, width=9)
    d.ellipse((319, 548+bob, 331, 560+bob), fill=(247, 200, 61), outline=INK, width=2)
    return im

progress = [0, .18, .37, .55, .72, .88, 1, 1, 1, 1, 1, 1]
frames = [make_frame(p, blink=(i == 9)) for i, p in enumerate(progress)]
durations = [110, 110, 120, 130, 140, 180] + [420] * 6
frames[0].save(OUT, save_all=True, append_images=frames[1:], duration=durations, loop=0, disposal=2)
print(OUT)
