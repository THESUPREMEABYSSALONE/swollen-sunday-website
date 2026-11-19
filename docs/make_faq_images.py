"""Rebuild the ten FAQ cards in the site's navy/gold style.

Run from the project root:
    python docs/make_faq_images.py

The originals are copied to docs/faq-originals/ the first time this runs,
then images/faq.jpeg and images/faq1..9.jpeg are replaced with corrected
versions that name the University of Ghana (UG) Stadium.

Why: the supplied artwork said "Independence Square, Accra" on two cards and
gave the start time as 2 PM, which disagreed with the rest of the site.
"""

import os
import shutil

from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(BASE, "images")
BACKUP = os.path.join(BASE, "docs", "faq-originals")
TMP_FONT = r"C:\Users\hp\AppData\Local\Temp\opencode\fonts\Anton-Regular.ttf"

W, H = 900, 1260

NAVY = (11, 30, 61)
DARK = (6, 18, 37)
GOLD = (212, 161, 42)
WHITE = (255, 255, 255)
LIGHT = (216, 226, 240)
MUTED = (150, 168, 190)
LINE = (40, 60, 90)

HEAD = (os.path.join(BASE, "docs", "fonts", "Anton-Regular.ttf")
        if os.path.exists(os.path.join(BASE, "docs", "fonts", "Anton-Regular.ttf"))
        else (TMP_FONT if os.path.exists(TMP_FONT) else r"C:\Windows\Fonts\ariblk.ttf"))
BODY = r"C:\Windows\Fonts\segoeui.ttf"
BOLD = r"C:\Windows\Fonts\segoeuib.ttf"

VENUE = "UNIVERSITY OF GHANA (UG) STADIUM  \u00b7  LEGON"
DATE = "15 NOV 2026"


def font(path, size):
    return ImageFont.truetype(path, size)


def tracked(draw, text, fnt, fill, x, y, space=3):
    """Draw text with extra space between letters (like letter-spacing)."""
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + space


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, line = [], ""
    for word in words:
        trial = (line + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not line:
            line = trial
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def draw_block(draw, text, fnt, fill, x, y, max_w, leading):
    lines = wrap(draw, text, fnt, max_w)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def background():
    """Navy gradient with a soft gold ring and a faint question mark."""
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=(
            int(14 - 8 * t), int(34 - 16 * t), int(70 - 33 * t)))
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.ellipse((-180, 780, 660, 1620), outline=GOLD + (26,), width=3)
    ld.ellipse((520, 900, 1160, 1540), outline=GOLD + (18,), width=2)
    img = Image.alpha_composite(img.convert("RGBA"), layer).convert("RGB")
    return img


def frame(img, number):
    """Shared header and footer used on every card."""
    d = ImageDraw.Draw(img)
    tracked(d, "SWOLLEN SUNDAY 2026", font(BOLD, 24), GOLD, 64, 64, 4)
    num = "%02d / 10" % number
    f = font(BOLD, 24)
    d.text((836 - d.textlength(num, font=f), 64), num, font=f, fill=MUTED)
    d.line([(64, 118), (836, 118)], fill=LINE, width=2)
    d.line([(64, 1136), (836, 1136)], fill=LINE, width=2)
    tracked(d, VENUE, font(BOLD, 18), GOLD, 64, 1168, 2)
    f2 = font(BODY, 18)
    d.text((836 - d.textlength(DATE, font=f2), 1168), DATE, font=f2, fill=MUTED)
    return d


def add_band(img):
    """Tinted stadium strip along the bottom, faded into the navy."""
    band_h = 300
    src = Image.open(os.path.join(IMG, "stadium4k.jpeg")).convert("RGB")
    new_w = W
    new_h = int(src.height * new_w / src.width)
    src = src.resize((new_w, new_h))
    top = max(0, (new_h - band_h) // 2)
    band = src.crop((0, top, W, top + band_h))
    band = Image.blend(band, Image.new("RGB", band.size, NAVY), 0.55).convert("RGBA")

    mask = Image.new("L", band.size, 0)
    md = ImageDraw.Draw(mask)
    for y in range(band_h):
        md.line([(0, y), (W, y)], fill=int(225 * (y / band_h) ** 1.35))
    band.putalpha(mask)
    img.paste(band, (0, 1136 - band_h), band)
    return img


def qa_card(number, question, answer):
    img = add_band(background())
    d = frame(img, number)
    qx, qy, qw = 182, 165, 654

    size = 50
    while True:
        fq = font(HEAD, size)
        lines = wrap(d, question, fq, qw)
        if len(lines) * (size + 8) <= 330 or size <= 38:
            break
        size -= 2
    leading = int(size * 1.16)
    d.rounded_rectangle((64, qy + 4, 148, qy + 88), radius=20, fill=GOLD)
    d.text((80, qy + 6), "Q", font=font(HEAD, 58), fill=NAVY)
    y = qy
    for line in lines:
        d.text((qx, y), line, font=fq, fill=WHITE)
        y += leading

    ay = max(380, y + 60)
    d.rounded_rectangle((64, ay + 4, 148, ay + 88), radius=20, outline=GOLD, width=3)
    d.text((82, ay + 12), "A", font=font(HEAD, 54), fill=GOLD)

    size = 36
    while size >= 28:
        fa = font(BODY, size)
        lead = int(size * 1.55)
        total = len(wrap(d, answer, fa, qw)) * lead
        if ay + total <= 1090:
            break
        size -= 2
    draw_block(d, answer, font(BODY, size), LIGHT, qx, ay + 2, qw, int(size * 1.55))
    return img


def list_card(number, question, items):
    img = add_band(background())
    d = frame(img, number)
    qx, qy, qw = 182, 165, 654
    fq = font(HEAD, 50)
    d.rounded_rectangle((64, qy + 4, 148, qy + 88), radius=20, fill=GOLD)
    d.text((80, qy + 6), "Q", font=font(HEAD, 58), fill=NAVY)
    y = qy
    for line in wrap(d, question, fq, qw):
        d.text((qx, y), line, font=fq, fill=WHITE)
        y += 58

    ay = max(380, y + 60)
    d.rounded_rectangle((64, ay + 4, 148, ay + 88), radius=20, outline=GOLD, width=3)
    d.text((82, ay + 12), "A", font=font(HEAD, 54), fill=GOLD)

    fy = ay + 10
    body = font(BODY, 34)
    for item in items:
        # gold diamond bullet (the font has no reliable star glyph)
        cy = fy + 28
        d.polygon([(194, cy - 9), (203, cy), (194, cy + 9), (185, cy)], fill=GOLD)
        fy = draw_block(d, item, body, LIGHT, 224, fy, 612, 48) + 14
    return img


def banner_card():
    img = background()
    d = ImageDraw.Draw(img)
    tracked(d, "QUESTIONS ANSWERED", font(BOLD, 24), GOLD, 64, 64, 4)
    num = "01 / 10"
    f = font(BOLD, 24)
    d.text((836 - d.textlength(num, font=f), 64), num, font=f, fill=MUTED)
    d.line([(64, 118), (836, 118)], fill=LINE, width=2)

    fb = font(HEAD, 116)
    d.text((60, 220), "SWOLLEN", font=fb, fill=WHITE)
    d.text((60, 338), "SUNDAY", font=fb, fill=WHITE)
    fq = font(HEAD, 190)
    d.text((54, 470), "FAQs", font=fq, fill=GOLD)

    d.line([(64, 760), (250, 760)], fill=GOLD, width=5)
    draw_block(d, "Everything you asked about the gathering at UG Stadium, answered.",
               font(BODY, 34), LIGHT, 64, 805, 760, 52)

    # swipe chip
    chip_font = font(BOLD, 22)
    label = "SWIPE TO READ  \u2192"
    cw = d.textlength(label, font=chip_font) + 56
    d.rounded_rectangle((64, 930, 64 + cw, 986), radius=28, outline=GOLD, width=2)
    d.text((92, 944), label, font=chip_font, fill=GOLD)

    d.line([(64, 1136), (836, 1136)], fill=LINE, width=2)
    tracked(d, VENUE, font(BOLD, 18), GOLD, 64, 1168, 2)
    f2 = font(BODY, 18)
    d.text((836 - d.textlength(DATE, font=f2), 1168), DATE, font=f2, fill=MUTED)
    return img


def closing_card():
    img = background()
    d = frame(img, 10)
    tracked(d, "STILL CONFUSED?", font(BOLD, 24), GOLD, 64, 190, 4)
    d.text((60, 250), "SEND US", font=font(HEAD, 110), fill=WHITE)
    d.text((60, 372), "A DM.", font=font(HEAD, 140), fill=GOLD)
    draw_block(d, "Message the team and someone will help you find your way "
                  "to the stadium, the bus or the next service.",
               font(BODY, 34), LIGHT, 64, 600, 740, 54)

    d.line([(64, 800), (250, 800)], fill=GOLD, width=5)
    tracked(d, "WHATSAPP", font(BOLD, 20), MUTED, 64, 840, 3)
    d.text((64, 874), "053 050 2572", font=font(HEAD, 56), fill=WHITE)

    d.line([(64, 1010), (250, 1010)], fill=GOLD, width=5)
    draw_block(d, "First Love Center, East Legon (Near UPSA), Accra.",
               font(BODY, 26), MUTED, 64, 1042, 700, 38)
    return img


CARDS = [
    (2, "WHAT IS SWOLLEN SUNDAY?",
     "Swollen Sunday is a Sunday where the whole church is mobilised to win souls "
     "and invite people to church."),
    (3, "WHERE WILL SWOLLEN SUNDAY TAKE PLACE?",
     "Swollen Sunday was held at the University of Ghana (UG) Stadium, Legon, Accra."),
    (4, "WILL THERE BE PARKING AVAILABLE AT UG STADIUM?",
     "Yes. There is ample parking at the stadium, and our team will be on-site to "
     "guide cars and keep traffic flowing. Please arrive early to secure a "
     "convenient spot."),
    (5, "CAN I BRING MY CHILDREN ALONG?",
     "Absolutely! Swollen Sunday is a family-friendly gathering. There is a safe, "
     "welcoming environment for children, and you are encouraged to come with "
     "your family."),
    (6, "ARE THERE BUSES AVAILABLE? WHERE IS THE GATHERING POINT?",
     "Yes! Free buses run from various locations across Accra to make transport "
     "easy. Designated gathering points are shared by your Basonta or fellowship "
     "leader. If you are not sure where to join a bus, send us a DM!"),
    (7, "DO I NEED TO REGISTER OR GET A TICKET?",
     "No registration or ticket is needed. Just come with your friends, family, "
     "and a heart ready for an encounter with God."),
    (8, "WHAT TIME SHOULD I ARRIVE?",
     "The event starts promptly at 3:00 PM. Arriving ahead of time helps you "
     "settle, find good seating, and enjoy the full experience."),
]

LIST_ITEMS = [
    "An umbrella (just in case)",
    "Your Bible",
    "A notebook and pen",
    "5 friends who need to be at Swollen Sunday with you",
]


def main():
    os.makedirs(BACKUP, exist_ok=True)
    originals = ["faq.jpeg"] + ["faq%d.jpeg" % i for i in range(1, 10)]
    for name in originals:
        src = os.path.join(IMG, name)
        dst = os.path.join(BACKUP, name)
        if os.path.exists(src) and not os.path.exists(dst):
            shutil.copy2(src, dst)

    out = [("faq.jpeg", banner_card())]
    for number, question, answer in CARDS:
        idx = number - 1
        out.append(("faq%d.jpeg" % idx, qa_card(number, question, answer)))
    out.append(("faq8.jpeg", list_card(9, "WHAT SHOULD I BRING?", LIST_ITEMS)))
    out.append(("faq9.jpeg", closing_card()))

    for name, img in out:
        path = os.path.join(IMG, name)
        img.save(path, "JPEG", quality=90, optimize=True, progressive=True)
        print("wrote", name, os.path.getsize(path) // 1024, "KB")


if __name__ == "__main__":
    main()
