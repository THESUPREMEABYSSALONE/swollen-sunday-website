"""Build docs/Swollen_Sunday_Group_Presentation.pptx.

Run from the project root:
    python docs/make_pptx.py

The deck is 16:9, uses the same navy/gold palette as the website, and puts a
short, plain-English script in the speaker notes of every slide.
"""

import os

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "docs", "Swollen_Sunday_Group_Presentation.pptx")

NAVY = RGBColor(0x0B, 0x1E, 0x3D)
DARK = RGBColor(0x06, 0x12, 0x25)
GOLD = RGBColor(0xD4, 0xA1, 0x2A)
SKY = RGBColor(0x4F, 0xB3, 0xE8)
LIGHT = RGBColor(0xF4, 0xF7, 0xFC)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GREY = RGBColor(0x5B, 0x6B, 0x83)
LINE = RGBColor(0xDB, 0xE4, 0xF0)
GREEN = RGBColor(0x25, 0xD3, 0x66)
PALE_GOLD = RGBColor(0xF7, 0xEE, 0xD6)

HEAD_FONT = "Arial Black"
BODY_FONT = "Segoe UI"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]


# ------------------------------------------------------------------ helpers
def slide_new(bg=WHITE):
    s = prs.slides.add_slide(BLANK)
    fill = s.background.fill
    fill.solid()
    fill.fore_color.rgb = bg
    return s


def text(slide, value, left, top, width, height, size=14, bold=False,
         color=NAVY, font=BODY_FONT, align=PP_ALIGN.LEFT,
         anchor=MSO_ANCHOR.TOP, spacing=1.0, italic=False):
    box = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    p = tf.paragraphs[0]
    p.alignment = align
    p.line_spacing = spacing
    run = p.add_run()
    run.text = value
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    run.font.name = font
    return box


def rect(slide, left, top, width, height, fill=None, line=None, radius=0.08,
         line_width=1.0, shape=MSO_SHAPE.ROUNDED_RECTANGLE):
    box = slide.shapes.add_shape(shape, Inches(left), Inches(top), Inches(width), Inches(height))
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        try:
            box.adjustments[0] = radius
        except Exception:
            pass
    if fill is None:
        box.fill.background()
    else:
        box.fill.solid()
        box.fill.fore_color.rgb = fill
    if line is None:
        box.line.fill.background()
    else:
        box.line.color.rgb = line
        box.line.width = Pt(line_width)
    box.shadow.inherit = False
    return box


def box_text(shape, value, size=9, color=NAVY, bold=False, font=BODY_FONT,
             align=PP_ALIGN.CENTER):
    tf = shape.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.05)
    tf.margin_right = Inches(0.05)
    tf.margin_top = Inches(0.02)
    tf.margin_bottom = Inches(0.02)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = value
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = font


def header(slide, kicker, title, number=None):
    rect(slide, 0.62, 0.52, 0.1, 0.72, fill=GOLD, radius=0.4)
    text(slide, kicker.upper(), 0.9, 0.5, 10.5, 0.28, size=10.5, bold=True,
         color=GOLD, spacing=1.0)
    text(slide, title, 0.88, 0.76, 11.6, 0.62, size=27, bold=True, font=HEAD_FONT,
         color=NAVY)
    rect(slide, 0.62, 1.46, 12.1, 0.02, fill=LINE, radius=0, shape=MSO_SHAPE.RECTANGLE)
    if number is not None:
        text(slide, f"{number:02d}", 11.9, 0.5, 0.85, 0.35, size=12, bold=True,
             color=RGBColor(0xC3, 0xCE, 0xDE), align=PP_ALIGN.RIGHT)


def footer(slide, number):
    text(slide, "Swollen Sunday 2026  ·  Group Presentation", 0.62, 7.08, 8.0, 0.25,
         size=9, color=RGBColor(0x9A, 0xA8, 0xBC))
    text(slide, str(number), 12.3, 7.05, 0.45, 0.28, size=9, bold=True,
         color=RGBColor(0x9A, 0xA8, 0xBC), align=PP_ALIGN.RIGHT)


def bullets(slide, items, left, top, width, height, size=15, gap=0.1,
            color=NAVY, bullet_color=GOLD):
    """One text box, one paragraph per bullet, so long lines never overlap."""
    tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    for index, item in enumerate(items):
        if isinstance(item, tuple):
            lead, rest = item
        else:
            lead, rest = None, item
        p = tf.paragraphs[0] if index == 0 else tf.add_paragraph()
        p.line_spacing = 1.1
        p.space_after = Pt(gap * 72)
        # hanging indent so wrapped lines line up under the text, not the bullet
        pPr = p._p.get_or_add_pPr()
        pPr.set("marL", "274320")
        pPr.set("indent", "-274320")
        dot = p.add_run()
        dot.text = "\u2022  "
        dot.font.bold = True
        dot.font.size = Pt(size)
        dot.font.color.rgb = bullet_color
        dot.font.name = BODY_FONT
        if lead:
            r1 = p.add_run()
            r1.text = lead + " "
            r1.font.bold = True
            r1.font.size = Pt(size)
            r1.font.color.rgb = color
            r1.font.name = BODY_FONT
        r2 = p.add_run()
        r2.text = rest
        r2.font.size = Pt(size)
        r2.font.color.rgb = color if lead else GREY
        r2.font.name = BODY_FONT


def note(slide, message):
    slide.notes_slide.notes_text_frame.text = message


def chip(slide, label, left, top, width, fill=LIGHT, color=NAVY, size=10):
    sh = rect(slide, left, top, width, 0.42, fill=fill, radius=0.4)
    box_text(sh, label, size=size, color=color, bold=True)
    return sh


# ==================================================================
# 1. TITLE
# ==================================================================
s = slide_new(NAVY)
rect(s, 0, 0, 13.333, 0.16, fill=GOLD, radius=0, shape=MSO_SHAPE.RECTANGLE)
rect(s, 0.85, 1.55, 0.12, 1.5, fill=GOLD, radius=0.3)
text(s, "FIRST LOVE CHURCH  ·  POST-EVENT RECAP WEBSITE", 1.2, 1.5, 10.8, 0.35,
     size=12, bold=True, color=SKY)
text(s, "Swollen Sunday 2026", 1.15, 1.95, 11.4, 1.0, size=54, bold=True,
     font=HEAD_FONT, color=WHITE)
text(s, "Building an immersive recap site with HTML5 and CSS3 only", 1.2, 3.0, 10.8, 0.55,
     size=20, color=RGBColor(0xD8, 0xE2, 0xF0))
rect(s, 1.2, 3.78, 2.2, 0.04, fill=GOLD, radius=0, shape=MSO_SHAPE.RECTANGLE)
text(s, "Level 200 Web Design Project  ·  4-Week Build", 1.2, 4.0, 8.0, 0.4,
     size=14, color=RGBColor(0xB9, 0xC6, 0xD8))
text(s, "Group members: [EDIT]  ·  Lecturer: [EDIT]  ·  Date: [EDIT]", 1.2, 4.42, 10.8, 0.4,
     size=12, color=RGBColor(0x8D, 0x9E, 0xB6))
chip(s, "30 photos", 1.2, 5.55, 1.55, fill=RGBColor(0x16, 0x2C, 0x51), color=WHITE)
chip(s, "16 videos", 2.9, 5.55, 1.55, fill=RGBColor(0x16, 0x2C, 0x51), color=WHITE)
chip(s, "2 pages", 4.6, 5.55, 1.45, fill=RGBColor(0x16, 0x2C, 0x51), color=WHITE)
chip(s, "1 stylesheet", 6.2, 5.55, 1.75, fill=RGBColor(0x16, 0x2C, 0x51), color=WHITE)
chip(s, "zero JavaScript*", 8.1, 5.55, 2.2, fill=RGBColor(0x16, 0x2C, 0x51), color=WHITE)
text(s, "* except the contact-form script supplied by the lecturer", 1.2, 6.3, 8.0, 0.3,
     size=10, color=RGBColor(0x8D, 0x9E, 0xB6), italic=True)
note(s, "Good morning. We are group [EDIT] and this is our Swollen Sunday 2026 recap website. "
        "It is a two-page site built with HTML and CSS only. In the next few minutes we will show "
        "the client's problem, our design, the code behind it, and what we tested.")

# ==================================================================
# 2. PROJECT OVERVIEW
# ==================================================================
s = slide_new()
header(s, "Project overview", "One site that keeps the momentum alive", 2)
bullets(s, [
    ("Goal:", "a single place to relive Swollen Sunday 2026 and take the next step."),
    ("Two pages:", "index.html tells the story and captures messages; gallery.html holds all the media."),
    ("Media:", "30 photographs and 16 videos supplied by the church."),
    ("Technology:", "HTML5 + CSS3 only. No framework, no database, no build tools."),
    ("Audience:", "students who attended, first-time visitors, and members looking for a branch."),
    ("Approach:", "mobile-first, tested at 360px, 768px and 1280px."),
], 0.72, 1.78, 7.6, 5.0, size=15)

# right stat card
rect(s, 8.75, 1.8, 3.95, 4.85, fill=LIGHT, line=LINE)
text(s, "AT A GLANCE", 9.05, 2.02, 3.4, 0.3, size=10, bold=True, color=GOLD)
stats = [("2", "HTML pages"), ("1", "CSS file"), ("30", "photos"), ("16", "videos"), ("0", "databases")]
y = 2.45
for big, small in stats:
    text(s, big, 9.05, y, 0.9, 0.62, size=30, bold=True, font=HEAD_FONT, color=NAVY)
    text(s, small, 10.05, y + 0.16, 2.4, 0.35, size=12, color=GREY)
    y += 0.82
note(s, "Our goal was simple: after November 15, people should still be able to feel the day. "
        "The site has two pages, uses only two files of code, and carries every photo and video the client gave us.")

# ==================================================================
# 3. CLIENT SCENARIO
# ==================================================================
s = slide_new(LIGHT)
header(s, "Client scenario", "The event is over. The story is not.", 3)
rect(s, 0.62, 1.8, 5.7, 3.55, fill=WHITE, line=LINE)
text(s, "THE CLIENT", 0.9, 2.02, 4.0, 0.3, size=10, bold=True, color=GOLD)
bullets(s, [
    ("First Love Church,", "East Legon, Accra."),
    ("Event:", "Swollen Sunday 2026, UG Stadium, Legon."),
    ("Date:", "Sunday 15 November 2026, 3:00–6:30 PM GMT."),
    ("Hosts:", "Dag Heward-Mills / Joshua Dag Heward-Mills."),
    ("Media:", "30 photos and 16 video clips, shot on the day."),
], 0.9, 2.4, 5.15, 2.8, size=13.5, gap=0.08)

rect(s, 6.62, 1.8, 6.1, 3.55, fill=WHITE, line=LINE)
text(s, "THE BRIEF", 6.9, 2.02, 4.0, 0.3, size=10, bold=True, color=GOLD)
bullets(s, [
    ("Problem:", "the gathering is finished, so the excitement disappears from the timeline."),
    ("Need:", "a permanent recap that also points people to church."),
    ("Must include:", "recap videos, photo gallery, FAQs, service times, a contact form."),
    ("Constraint:", "beginner-friendly code with no frameworks and no JavaScript."),
    ("Success:", "a visitor can watch, look, read and plan a visit in under two minutes."),
], 6.9, 2.4, 5.5, 2.8, size=13.5, gap=0.08)

rect(s, 0.62, 5.65, 12.1, 0.95, fill=NAVY, line=NAVY)
text(s, "One page to relive the night.   One page to prove it happened.   One button to plan the next visit.",
     0.95, 5.9, 11.4, 0.45, size=14.5, bold=True, color=WHITE)
note(s, "The church came to us with a clear problem. The stadium was full on Sunday, but by Monday the "
        "momentum was gone. They wanted a site that keeps the memory alive and, more importantly, "
        "moves a visitor to attend a service. Everything on the page points to that next step.")

# ==================================================================
# 4. WIREFRAME — HOME
# ==================================================================
s = slide_new()
header(s, "Wireframe", "Home page: one long story, top to bottom", 4)

W, X, Y = 7.35, 0.62, 1.62


def wb(y, h, label, x=X, w=W, fill=LIGHT, color=GREY, size=8, line=LINE):
    b = rect(s, x, y, w, h, fill=fill, line=line, radius=0.05)
    box_text(b, label, size=size, color=color, bold=True)
    return y + h + 0.055


y = Y
y = wb(y, 0.22, "NAVBAR  ·  logo + 6 links", fill=NAVY, color=WHITE, line=NAVY)
y = wb(y, 0.68, "HERO  ·  crossfading photos + dark overlay + headline + 2 buttons", fill=RGBColor(0x14, 0x2A, 0x4D), color=WHITE, line=NAVY)
# three video boxes inside the strip
strip_top = y
rect(s, X, strip_top, W, 0.44, fill=RGBColor(0xE8, 0xEF, 0xF9), line=LINE, radius=0.05)
text(s, "RECAP VIDEO STRIP", X + 0.1, strip_top + 0.14, 1.8, 0.2,
     size=7.5, bold=True, color=GREY)
for k, clip in enumerate(["pixelad", "swollenhistory", "Venuehistory"]):
    vb = rect(s, X + 1.95 + k * 1.8, strip_top + 0.07, 1.7, 0.3, fill=WHITE, line=LINE, radius=0.1)
    box_text(vb, clip, size=6.5, color=GREY)
y = strip_top + 0.44 + 0.055
# about split
rect(s, X, y, 3.4, 0.52, fill=WHITE, line=LINE, radius=0.05)
rect(s, X + 3.55, y, 3.8, 0.52, fill=LIGHT, line=LINE, radius=0.05)
text(s, "ABOUT  ·  text + button", X + 0.1, y + 0.16, 3.2, 0.22, size=8, bold=True, color=GREY)
text(s, "PHOTO COLLAGE  ·  4 pictures", X + 3.65, y + 0.16, 3.6, 0.22, size=8, bold=True, color=GREY)
y += 0.52 + 0.055
# highlights
for k in range(3):
    rect(s, X + k * 2.47, y, 2.39, 0.3, fill=PALE_GOLD, line=LINE, radius=0.1)
    text(s, ["VIBRANT WORSHIP", "THE WORD", "REAL COMMUNITY"][k], X + k * 2.47, y + 0.06, 2.39, 0.2,
         size=7.5, bold=True, color=NAVY, align=PP_ALIGN.CENTER)
y += 0.3 + 0.055
# pastors
rect(s, X, y, 3.3, 0.42, fill=NAVY, line=NAVY, radius=0.05)
text(s, "PASTORS  ·  history video", X + 0.1, y + 0.11, 3.1, 0.2, size=7.5, bold=True, color=WHITE)
for k in range(4):
    rect(s, X + 3.45 + (k % 4) * 0.97, y, 0.88, 0.42, fill=LIGHT, line=LINE, radius=0.1)
y += 0.42 + 0.055
# gallery preview
rect(s, X, y, W, 0.52, fill=WHITE, line=LINE, radius=0.05)
for k in range(4):
    rect(s, X + 0.08 + k * 0.62, y + 0.06, 0.56, 0.18, fill=RGBColor(0xDD, 0xE6, 0xF2), line=LINE, radius=0.1)
    rect(s, X + 0.08 + k * 0.62, y + 0.28, 0.56, 0.18, fill=RGBColor(0xDD, 0xE6, 0xF2), line=LINE, radius=0.1)
text(s, "GALLERY PREVIEW  ·  8 photos  +  See Full Gallery", X + 2.7, y + 0.16, 4.5, 0.2, size=8, bold=True, color=GREY)
y += 0.52 + 0.055
# event info
rect(s, X, y, 3.58, 0.42, fill=WHITE, line=GOLD, radius=0.05, line_width=1.5)
rect(s, X + 3.77, y, 3.58, 0.42, fill=NAVY, line=NAVY, radius=0.05)
text(s, "EVENT ARCHIVE", X + 0.1, y + 0.11, 3.3, 0.2, size=7.5, bold=True, color=GREY)
text(s, "WHAT'S NEXT", X + 3.87, y + 0.11, 3.3, 0.2, size=7.5, bold=True, color=WHITE)
y += 0.42 + 0.04
rect(s, X, y, W, 0.16, fill=RGBColor(0xE4, 0xE9, 0xF1), line=LINE, radius=0.2)
text(s, "GOOGLE MAP  ·  grayscale until hover", X + 0.1, y + 0.0, 4.0, 0.16, size=6.5, color=GREY)
y += 0.16 + 0.055
# schedule
rect(s, X, y, W, 0.42, fill=WHITE, line=LINE, radius=0.05)
text(s, "SCHEDULE", X + 0.1, y + 0.13, 1.7, 0.2, size=7.5, bold=True, color=GREY)
for k in range(4):
    sb = rect(s, X + 1.95 + k * 1.35, y + 0.06, 1.28, 0.3, fill=LIGHT, line=LINE, radius=0.1)
    box_text(sb, "NOV 22", size=6.5, color=GREY, bold=True)
y += 0.42 + 0.055
# faq
rect(s, X, y, W, 0.36, fill=WHITE, line=LINE, radius=0.05)
text(s, "FAQ", X + 0.1, y + 0.09, 1.4, 0.18, size=7.5, bold=True, color=GREY)
for k in range(5):
    rect(s, X + 1.95 + k * 1.05, y + 0.07, 0.95, 0.22, fill=PALE_GOLD, line=LINE, radius=0.1)
y += 0.36 + 0.055
# contact
rect(s, X, y, 3.3, 0.34, fill=WHITE, line=LINE, radius=0.05)
rect(s, X + 3.5, y, 3.85, 0.34, fill=RGBColor(0xE8, 0xEF, 0xF9), line=LINE, radius=0.05)
text(s, "CONTACT DETAILS", X + 0.1, y + 0.08, 3.0, 0.18, size=7, bold=True, color=GREY)
text(s, "FORM  ·  name, phone, topic, message", X + 3.6, y + 0.08, 3.6, 0.18, size=7, bold=True, color=GREY)
y += 0.34 + 0.055
rect(s, X, y, W, 0.26, fill=NAVY, line=NAVY, radius=0.05)
text(s, "FOOTER  ·  4 columns + copyright bar", X + 0.12, y + 0.05, 6.0, 0.18, size=7, bold=True, color=WHITE)

# right legend
rect(s, 8.35, 1.72, 4.35, 4.95, fill=LIGHT, line=LINE)
text(s, "READING THE SKETCH", 8.6, 1.95, 4.0, 0.28, size=10, bold=True, color=GOLD)
text(s, "The page works like a sales conversation:", 8.6, 2.32, 3.85, 0.3, size=12, bold=True, color=NAVY)
steps = [("1", "Catch attention", "hero photo and headline"),
         ("2", "Build trust", "about, pastors, videos"),
         ("3", "Show proof", "gallery and FAQs"),
         ("4", "Answer questions", "event details and schedule"),
         ("5", "Ask for action", "contact form and WhatsApp")]
yy = 2.78
for n, t1, t2 in steps:
    circ = rect(s, 8.6, yy, 0.34, 0.34, fill=GOLD, line=None, radius=0.5, shape=MSO_SHAPE.OVAL)
    box_text(circ, n, size=10, bold=True, color=NAVY)
    text(s, t1, 9.08, yy - 0.02, 3.2, 0.26, size=11.5, bold=True, color=NAVY)
    text(s, t2, 9.08, yy + 0.23, 3.2, 0.25, size=9.5, color=GREY)
    yy += 0.72
note(s, "This is our paper sketch before any code. Every box is one section. Notice the order: grab attention, "
        "build trust, show proof, answer questions, then ask for an action. The design is one long page so a visitor "
        "never has to hunt for information.")

# ==================================================================
# 5. WIREFRAME — GALLERY + MOBILE
# ==================================================================
s = slide_new()
header(s, "Wireframe", "Gallery page, and the same site on a phone", 5)

gx, gw = 0.7, 7.1
yy = 1.75
b = rect(s, gx, yy, gw, 0.4, fill=NAVY, line=NAVY, radius=0.05)
box_text(b, "NAVBAR  ·  same six links, Gallery marked active", size=8.5, color=WHITE, bold=True)
yy += 0.46
b = rect(s, gx, yy, gw, 0.6, fill=RGBColor(0x14, 0x2A, 0x4D), line=NAVY, radius=0.05)
box_text(b, "PAGE TITLE  ·  eyebrow + h1 + one-line intro", size=9, color=WHITE, bold=True)
yy += 0.66
text(s, "PHOTOS  ·  20 images", gx, yy, 4.0, 0.25, size=9, bold=True, color=GOLD)
yy += 0.3
for row in range(3):
    for col in range(4):
        rect(s, gx + col * 1.79, yy + row * 0.52, 1.68, 0.45, fill=RGBColor(0xDD, 0xE6, 0xF2), line=LINE, radius=0.08)
yy += 3 * 0.52 + 0.15
text(s, "VIDEOS  ·  15 clips  ·  controls + preload=metadata", gx, yy, 5.5, 0.25, size=9, bold=True, color=GOLD)
yy += 0.3
for row in range(2):
    for col in range(3):
        rect(s, gx + col * 2.4, yy + row * 0.5, 2.28, 0.42, fill=RGBColor(0xE8, 0xEF, 0xF9), line=LINE, radius=0.08)
yy += 2 * 0.5 + 0.12
b = rect(s, gx, yy, gw, 0.3, fill=NAVY, line=NAVY, radius=0.05)
box_text(b, "FOOTER", size=8, color=WHITE, bold=True)

# phone frame
px, py, pw, ph = 8.85, 1.7, 2.35, 5.0
phone = rect(s, px, py, pw, ph, fill=WHITE, line=NAVY, radius=0.12, line_width=2)
rect(s, px + 0.78, py + 0.1, 0.8, 0.06, fill=LINE, radius=0.4)
iy = py + 0.26
iw = pw - 0.24
nav_bar = rect(s, px + 0.12, iy, iw, 0.34, fill=NAVY, radius=0.08)
box_text(nav_bar, "logo + wrapped nav (2 rows)", size=6, color=WHITE)
iy += 0.34 + 0.05
steps = [("HERO", 0.46, RGBColor(0x14, 0x2A, 0x4D), WHITE),
         ("1 video", 0.24, LIGHT, GREY),
         ("ABOUT text", 0.24, LIGHT, GREY),
         ("collage (2 cols)", 0.24, LIGHT, GREY),
         ("highlights", 0.2, PALE_GOLD, NAVY),
         ("pastors (2 x 2)", 0.24, LIGHT, GREY),
         ("gallery (1 col)", 0.3, LIGHT, GREY),
         ("event cards", 0.22, LIGHT, GREY),
         ("map", 0.16, RGBColor(0xE4, 0xE9, 0xF1), GREY),
         ("schedule", 0.22, LIGHT, GREY),
         ("FAQ swipe row", 0.2, PALE_GOLD, NAVY),
         ("contact form", 0.24, LIGHT, GREY)]
for label, h, fill, col in steps:
    rect(s, px + 0.12, iy, iw, h, fill=fill, line=LINE, radius=0.1)
    text(s, label, px + 0.16, iy + h / 2 - 0.07, iw - 0.08, 0.18, size=6, color=col, bold=True, align=PP_ALIGN.CENTER)
    iy += h + 0.045
foot = rect(s, px + 0.12, iy + 0.04, iw, 0.26, fill=NAVY, radius=0.1)
box_text(foot, "footer  ·  4 columns stacked", size=6, color=WHITE, bold=True)

text(s, "THE SAME FILE, THREE WIDTHS", 11.4, 1.95, 1.9, 0.5, size=8.5, bold=True, color=GOLD)
text(s, "360px", 11.4, 2.5, 1.85, 0.3, size=15, bold=True, font=HEAD_FONT, color=NAVY)
text(s, "one column", 11.4, 2.85, 1.85, 0.3, size=10, color=GREY)
text(s, "768px", 11.4, 3.55, 1.85, 0.3, size=15, bold=True, font=HEAD_FONT, color=NAVY)
text(s, "two columns", 11.4, 3.9, 1.85, 0.3, size=10, color=GREY)
text(s, "1024px+", 11.4, 4.6, 1.85, 0.3, size=15, bold=True, font=HEAD_FONT, color=NAVY)
text(s, "four photo columns", 11.4, 4.95, 1.85, 0.6, size=10, color=GREY)
text(s, "Nothing is hidden on mobile. It simply stacks.", 11.4, 5.85, 1.8, 0.9, size=9.5, italic=True, color=GREY)
note(s, "The gallery is the second page. Photos come first because they are the fastest thing to enjoy, then the videos. "
        "On the right is the same home page squeezed into a 360 pixel phone. Nothing new is designed for mobile: "
        "the columns simply stack. The menu wraps onto two lines instead of using a hamburger.")

# ==================================================================
# 6. FOLDER STRUCTURE
# ==================================================================
s = slide_new(LIGHT)
header(s, "Project files", "A small folder structure anyone can open", 6)

card = rect(s, 0.62, 1.78, 6.9, 4.55, fill=DARK, line=DARK)
text(s, "swollen-sunday-website/", 0.9, 1.98, 6.3, 0.32, size=14, bold=True, color=GOLD, font="Consolas")
tree = [
    ("├── index.html", "home page: story, videos, schedule, form"),
    ("├── gallery.html", "20 photos + 15 videos"),
    ("├── css/", ""),
    ("│   └── style.css", "the only stylesheet"),
    ("├── js/", ""),
    ("│   └── form.js", "lecturer's form script"),
    ("├── images/", "30 .jpeg files"),
    ("├── videos/", "16 .mp4 files"),
    ("└── docs/", "these study materials"),
]
yy = 2.4
for name, desc in tree:
    text(s, name, 0.95, yy, 3.0, 0.26, size=11.5, color=WHITE, font="Consolas")
    if desc:
        text(s, desc, 3.95, yy + 0.02, 3.3, 0.24, size=10, color=RGBColor(0x8D, 0x9E, 0xB6))
    yy += 0.39
rect(s, 0.95, 6.0, 6.25, 0.01, fill=RGBColor(0x2A, 0x3D, 0x5A), radius=0, shape=MSO_SHAPE.RECTANGLE)
text(s, "No frameworks  ·  no database  ·  no build tools", 0.95, 6.1, 6.2, 0.3,
     size=10, italic=True, color=RGBColor(0x8D, 0x9E, 0xB6))

bullets(s, [
    ("One stylesheet:", "style.css is linked in both pages, so a colour change happens once."),
    ("Relative paths:", "images/Group pic.jpeg is written images/Group%20pic.jpeg."),
    ("No spaces in URLs:", "%20 is the code for a space."),
    ("No build step:", "double-click index.html and it works."),
    ("Docs folder:", "keeps the explanation and slides away from the live site."),
], 7.85, 1.85, 4.9, 4.6, size=13, gap=0.12)
note(s, "The folder structure is deliberately simple. One CSS file, one placeholder script, two media folders. "
        "The only tricky part is spaces in file names: a browser cannot read a space, so we write %20. "
        "If you move a file, its link breaks, so we never rename the client's media.")

# ==================================================================
# 7. COLOURS AND FONTS
# ==================================================================
s = slide_new()
header(s, "Design system", "Five colours, two fonts, one place to change them", 7)

text(s, "COLOUR VARIABLES  (:root)", 0.7, 1.72, 6.0, 0.3, size=10, bold=True, color=GOLD)
swatches = [
    ("--primary", "#0B1E3D", "deep navy", NAVY, WHITE),
    ("--secondary", "#D4A12A", "gold", GOLD, DARK),
    ("--accent", "#4FB3E8", "sky blue", SKY, DARK),
    ("--light", "#F4F7FC", "page wash", LIGHT, NAVY),
    ("--dark", "#061225", "footer", DARK, WHITE),
]
yy = 2.12
for name, hexv, role, fill, txt in swatches:
    rect(s, 0.7, yy, 0.75, 0.62, fill=fill, line=LINE if fill == LIGHT else None, radius=0.1)
    text(s, name, 1.62, yy + 0.02, 2.0, 0.3, size=13, bold=True, color=NAVY, font="Consolas")
    text(s, hexv + "  ·  " + role, 1.62, yy + 0.3, 3.2, 0.26, size=10.5, color=GREY)
    yy += 0.78

rect(s, 0.7, 6.0, 5.9, 0.62, fill=LIGHT, line=LINE)
text(s, "Change a hex code once  →  the whole site re-skins.", 0.95, 6.17, 5.5, 0.3,
     size=11.5, bold=True, color=NAVY)

text(s, "TYPOGRAPHY", 7.0, 1.72, 5.0, 0.3, size=10, bold=True, color=GOLD)
rect(s, 7.0, 2.1, 5.7, 1.6, fill=LIGHT, line=LINE)
text(s, "Aa", 7.25, 2.22, 1.2, 0.9, size=44, bold=True, font=HEAD_FONT, color=NAVY)
text(s, "ANTON", 8.4, 2.3, 3.9, 0.32, size=13, bold=True, color=GOLD)
text(s, "Bold display headings. One weight only, so it is easy to use.", 8.4, 2.66, 4.0, 0.5,
     size=10.5, color=GREY)
text(s, "Used on every h1, h2 and the logo.", 8.4, 3.15, 4.0, 0.3, size=10, italic=True, color=GREY)

rect(s, 7.0, 3.9, 5.7, 1.6, fill=LIGHT, line=LINE)
text(s, "Aa", 7.25, 4.0, 1.2, 0.9, size=38, bold=True, color=NAVY)
text(s, "INTER", 8.4, 4.1, 3.9, 0.32, size=13, bold=True, color=GOLD)
text(s, "Clean body text in four weights: 400, 500, 600, 700.", 8.4, 4.46, 4.0, 0.5,
     size=10.5, color=GREY)
text(s, "Used for paragraphs, buttons, labels and the form.", 8.4, 4.95, 4.0, 0.3, size=10, italic=True, color=GREY)

rect(s, 7.0, 5.85, 5.7, 0.68, fill=NAVY, line=NAVY)
text(s, "Both loaded from Google Fonts  ·  Arial Black fallback", 7.2, 6.04, 5.4, 0.3,
     size=10, color=WHITE)
note(s, "The whole palette lives in :root at the top of style.css. When the course rep gives us the official "
        "brand colours, we change five values and the entire site follows. The fonts are Anton for headings and "
        "Inter for reading, both free from Google Fonts, with system fallbacks in case the internet is down.")

# ==================================================================
# 8. HTML SECTION 1
# ==================================================================
s = slide_new(LIGHT)
header(s, "The code — HTML", "Home page sections, part 1", 8)
bullets(s, [
    ("Semantic shell:", "header > nav, main > section, footer. No div soup."),
    ("Hero:", "three layers — slides, dark overlay, content. h1 appears once."),
    ("Video strip:", "video controls preload=metadata, source, fallback text."),
    ("About:", "figure + figcaption for the collage; three emoji highlights."),
    ("Pastors:", "four figure cards; captions marked [EDIT] because we never guess names."),
    ("Accessibility:", "alt on every image, aria-hidden on decoration, correct heading order."),
], 0.7, 1.8, 7.0, 4.9, size=14)

rect(s, 7.95, 1.78, 4.75, 4.95, fill=WHITE, line=LINE)
text(s, "SAMPLE  ·  HERO LAYERS", 8.2, 1.98, 4.0, 0.28, size=9.5, bold=True, color=GOLD)
code = ('<section class="hero" id="home">\n'
        '  <div class="hero-slides">\n'
        '    <div class="slide slide-1"></div>\n'
        '    ... 4 slides ...\n'
        '  </div>\n'
        '  <div class="hero-overlay"></div>\n'
        '  <div class="hero-content">\n'
        '    <h1>Thousands Gathered.</h1>\n'
        '    <a href="#recap-videos">\n'
        '      Watch the Recap Video\n'
        '    </a>\n'
        '  </div>\n'
        '</section>')
box = rect(s, 8.2, 2.38, 4.25, 3.2, fill=DARK, line=DARK, radius=0.05)
text(s, code, 8.35, 2.5, 3.95, 3.0, size=8.6, color=RGBColor(0xD8, 0xE2, 0xF0), font="Consolas")
text(s, "The photo divs are empty in HTML.", 8.2, 5.72, 4.3, 0.26, size=9.5, bold=True, color=NAVY)
text(s, "Their pictures are set in CSS, so the HTML stays clean.", 8.2, 5.98, 4.3, 0.55, size=9.5, color=GREY)
note(s, "We start the markup with meaning, not decoration. header, nav, main, section, article, figure and footer "
        "tell the browser and a screen reader what each block is. The hero is three stacked layers: four empty photo "
        "divs, a dark overlay, then the text. The photos are added in CSS so the HTML stays readable.")

# ==================================================================
# 9. HTML SECTION 2
# ==================================================================
s = slide_new()
header(s, "The code — HTML", "Home page sections, part 2", 9)
bullets(s, [
    ("Gallery preview:", "8 linked photos, target=_blank and rel=noopener."),
    ("Event info:", "two cards plus a Google Maps iframe with loading=lazy."),
    ("Schedule:", "4 cards, a date badge and a real Google Calendar link."),
    ("FAQ:", "banner + 9 cards in a scroll row; each card opens the full image."),
    ("Contact:", "label for / input id pairs, name attributes, required fields."),
    ("Footer:", "four columns, copyright bar, floating WhatsApp link."),
], 0.7, 1.8, 7.0, 4.9, size=14)

rect(s, 7.95, 1.78, 4.75, 4.95, fill=LIGHT, line=LINE)
text(s, "FORM FIELDS AND THEIR NAMES", 8.2, 1.98, 4.2, 0.28, size=9.5, bold=True, color=GOLD)
rows = [("Full Name", "text", "fullname"), ("Phone / WhatsApp", "tel", "phone"),
        ("How Can We Help?", "select", "topic"), ("Your Message", "textarea", "message")]
yy = 2.4
for label, kind, name in rows:
    rect(s, 8.2, yy, 4.25, 0.72, fill=WHITE, line=LINE, radius=0.08)
    text(s, label, 8.38, yy + 0.08, 2.2, 0.26, size=10.5, bold=True, color=NAVY)
    text(s, kind + "  ·  name=\"" + name + "\"", 8.38, yy + 0.36, 3.9, 0.24, size=9.5, color=GREY, font="Consolas")
    yy += 0.84
text(s, "The script finds each value by its name attribute.", 8.2, 5.85, 4.3, 0.5, size=9.5, color=GREY)

rect(s, 0.7, 5.55, 7.05, 0.9, fill=LIGHT, line=LINE)
text(s, "Two quick wins:", 0.95, 5.72, 2.0, 0.28, size=11, bold=True, color=NAVY)
text(s, "every image has alt text, and every section has an id so the menu can jump to it.",
     2.55, 5.72, 5.0, 0.55, size=10.5, color=GREY)
note(s, "The second half of the home page is about proof and action: photos, event facts, the schedule, the FAQs "
        "and the form. On the right you can see the four form fields. The name attribute matters because the "
        "lecturer's script reads exactly those names. The label's for attribute must match the input's id.")

# ==================================================================
# 10. CSS FOUNDATION
# ==================================================================
s = slide_new(LIGHT)
header(s, "The code — CSS", "Foundation: variables, reset and helpers", 10)
bullets(s, [
    ("Variables:", "five colours, a radius, a shadow and two fonts in :root."),
    ("Reset:", "* { box-sizing: border-box; margin: 0; padding: 0; }"),
    ("Base:", "body font and line-height; img/video max-width 100%; smooth scroll."),
    ("scroll-padding-top:", "stops the sticky navbar covering the heading you jumped to."),
    ("Helpers:", ".container, .eyebrow, .section-title, .section-lead, .btn."),
    ("Buttons:", "one base shape, then colour classes for gold, ghost, outline, WhatsApp."),
], 0.7, 1.8, 7.0, 4.9, size=14)

rect(s, 7.95, 1.78, 4.75, 4.95, fill=DARK, line=DARK)
text(s, "css/style.css  ·  TOP OF FILE", 8.2, 1.98, 4.2, 0.28, size=9.5, bold=True, color=GOLD)
code = (':root {\n'
        '  --primary: #0b1e3d;\n'
        '  --secondary: #d4a12a;\n'
        '  --accent: #4fb3e8;\n'
        '  --light: #f4f7fc;\n'
        '  --dark: #061225;\n'
        '  --radius: 18px;\n'
        '  --shadow: 0 12px 30px\n'
        '            rgba(11,30,61,.12);\n'
        '}\n\n'
        '.btn {\n'
        '  border-radius: 999px;\n'
        '  transition: transform .25s;\n'
        '}\n'
        '.btn:hover {\n'
        '  transform: translateY(-3px);\n'
        '}')
text(s, code, 8.2, 2.4, 4.3, 4.0, size=9.2, color=RGBColor(0xD8, 0xE2, 0xF0), font="Consolas")

rect(s, 0.7, 5.55, 6.9, 0.95, fill=PALE_GOLD, line=GOLD)
text(s, "Rule we followed:", 0.95, 5.72, 2.0, 0.28, size=11, bold=True, color=NAVY)
text(s, "no colour is ever typed twice in the file — it always comes from a variable.",
     2.85, 5.72, 4.6, 0.6, size=10.5, color=NAVY)
note(s, "This is the foundation every other rule stands on. The variables mean the client's colours can be swapped "
        "in seconds. The reset removes the browser's default spacing. The helper classes keep the HTML short: "
        "container centres content, eyebrow makes the small gold label, btn makes any link look like a button.")

# ==================================================================
# 11. CSS COMPONENTS / EFFECTS
# ==================================================================
s = slide_new()
header(s, "The code — CSS", "The effects that make it feel alive", 11)
bullets(s, [
    ("Sticky navbar:", "position: sticky; top: 0; z-index: 50."),
    ("Hero crossfade:", "4 slides, one 24s animation, delays of 0s, 6s, 12s, 18s."),
    ("Hover lift:", "transform: translateY(-6px) plus a deeper box-shadow."),
    ("Hover zoom:", "scale(1.08) inside overflow: hidden so the crop stays neat."),
    ("Reveal captions:", "opacity 0 → 1 and translateY(10px) → 0 on hover."),
    ("Focus ring:", "border-color: var(--accent) plus a 4px soft shadow."),
    ("4 keyframes:", "fadeSlide, fadeUp, glow, greenPulse."),
], 0.7, 1.8, 6.9, 5.0, size=13.5, gap=0.1)

# timeline graphic
rect(s, 7.9, 1.8, 4.8, 3.2, fill=LIGHT, line=LINE)
text(s, "HERO CROSSFADE TIMELINE", 8.15, 2.0, 4.2, 0.28, size=9.5, bold=True, color=GOLD)
labels = ["slide-1\n0s", "slide-2\n6s", "slide-3\n12s", "slide-4\n18s"]
fills = [NAVY, RGBColor(0x1B, 0x3A, 0x69), RGBColor(0x2A, 0x52, 0x8C), SKY]
for k in range(4):
    b = rect(s, 8.15 + k * 1.08, 2.42, 0.98, 0.95, fill=fills[k], line=None, radius=0.1)
    box_text(b, labels[k].split("\n")[0], size=8, color=WHITE, bold=True)
    text(s, labels[k].split("\n")[1], 8.15 + k * 1.08, 3.42, 0.98, 0.24, size=9, color=GREY, align=PP_ALIGN.CENTER)
rect(s, 8.2, 3.85, 4.2, 0.03, fill=LINE, radius=0, shape=MSO_SHAPE.RECTANGLE)
text(s, "24-second loop", 8.15, 3.95, 2.0, 0.25, size=9, bold=True, color=NAVY)
text(s, "Each photo fades in, holds for 25% of the cycle, then fades out.", 8.15, 4.22, 4.3, 0.55, size=9.5, color=GREY)

rect(s, 7.9, 5.25, 4.8, 1.4, fill=NAVY, line=NAVY)
text(s, "No JavaScript was used for any of this.", 8.15, 5.42, 4.3, 0.3, size=12, bold=True, color=WHITE)
text(s, "Hover, focus, animation and scrolling are all native CSS.", 8.15, 5.75, 4.3, 0.6, size=10, color=RGBColor(0xB9, 0xC6, 0xD8))

rect(s, 0.7, 5.85, 6.9, 0.75, fill=PALE_GOLD, line=GOLD)
text(s, "Two properties do most of the work:  transform  and  transition.", 0.95, 6.02, 6.4, 0.35,
     size=12, bold=True, color=NAVY)
note(s, "These are the small touches that make the page feel expensive without any JavaScript. The hero is four "
        "photos running the same 24 second animation, started at different times, so they crossfade. Cards lift on "
        "hover, photos zoom inside their frames, captions fade in, and the form shows a blue ring when you tab into it.")

# ==================================================================
# 12. FLEXBOX AND GRID
# ==================================================================
s = slide_new(LIGHT)
header(s, "Layout", "Flexbox for a line. Grid for a layout.", 12)

rect(s, 0.62, 1.76, 5.85, 4.15, fill=WHITE, line=LINE)
text(s, "FLEXBOX", 0.9, 1.96, 3.0, 0.34, size=13, bold=True, color=GOLD)
text(s, "One direction: a row or a column.", 0.9, 2.3, 5.2, 0.3, size=11, color=GREY)
for k in range(6):
    b = rect(s, 0.9 + k * 0.82, 2.8, 0.72, 0.42, fill=NAVY, line=None, radius=0.1)
    box_text(b, "link", size=8, color=WHITE)
text(s, "Navbar links wrap onto a second line.", 0.9, 3.3, 5.2, 0.26, size=9.5, color=GREY, italic=True)
for k in range(3):
    rect(s, 0.9 + k * 1.15, 3.85, 1.02, 0.62, fill=PALE_GOLD, line=GOLD, radius=0.1)
text(s, "Three highlight cards in a row.", 0.9, 4.55, 5.2, 0.26, size=9.5, color=GREY, italic=True)
code_txt = "display: flex;\njustify-content: center;\ngap: 14px;\nflex-wrap: wrap;"
text(s, code_txt, 0.9, 4.95, 5.2, 0.95, size=9.5, color=NAVY, font="Consolas")

rect(s, 6.82, 1.76, 5.9, 4.15, fill=WHITE, line=LINE)
text(s, "GRID", 7.1, 1.96, 3.0, 0.34, size=13, bold=True, color=GOLD)
text(s, "Two directions: rows and columns together.", 7.1, 2.3, 5.3, 0.3, size=11, color=GREY)
for row in range(2):
    for col in range(4):
        rect(s, 7.1 + col * 1.34, 2.85 + row * 0.8, 1.22, 0.7, fill=RGBColor(0xDD, 0xE6, 0xF2), line=LINE, radius=0.08)
text(s, "The photo gallery: 4 columns on desktop, 2 on tablet, 1 on phone.", 7.1, 4.5, 5.3, 0.26, size=9.5, color=GREY, italic=True)
code_txt2 = "display: grid;\ngrid-template-columns:\n  repeat(4, 1fr);\ngap: 14px;"
text(s, code_txt2, 7.1, 4.9, 5.3, 0.95, size=9.5, color=NAVY, font="Consolas")

rect(s, 0.62, 6.1, 12.1, 0.6, fill=NAVY, line=NAVY)
text(s, "Rule of thumb:  one direction  →  Flexbox          two directions  →  Grid", 0.9, 6.24, 11.5, 0.3,
     size=12.5, bold=True, color=WHITE)
note(s, "Students often ask which layout to use. The answer is in the shape of the content. A row of buttons or "
        "links is one direction, so Flexbox. A photo gallery or a page split has rows and columns at once, so Grid. "
        "Using the right one keeps the CSS short.")

# ==================================================================
# 13. RESPONSIVE
# ==================================================================
s = slide_new()
header(s, "Responsive design", "Mobile first, then only two breakpoints", 13)

cols = [("360px", "PHONE", 1, 1, 1), ("768px", "TABLET", 2, 2, 1), ("1024px+", "DESKTOP", 4, 3, 2)]
x = 0.62
for width, kind, photos, videos, split in cols:
    rect(s, x, 1.78, 3.85, 3.65, fill=LIGHT, line=LINE)
    text(s, kind, x + 0.28, 1.98, 3.3, 0.3, size=10, bold=True, color=GOLD)
    text(s, width, x + 0.28, 2.28, 3.3, 0.5, size=24, bold=True, font=HEAD_FONT, color=NAVY)
    rows = [("Photo grid", f"{photos} column" + ("s" if photos > 1 else "")),
            ("Video grid", f"{videos} column" + ("s" if videos > 1 else "")),
            ("Navbar", "wraps" if photos == 1 else "one row"),
            ("Page split", f"{split} column" + ("s" if split > 1 else "")),
            ("Footer", f"{photos if photos < 4 else 4} column" + ("s" if photos > 1 else ""))]
    yy = 2.86
    for label, value in rows:
        text(s, label, x + 0.28, yy, 1.9, 0.26, size=10, color=GREY)
        text(s, value, x + 2.1, yy, 1.55, 0.26, size=10, bold=True, color=NAVY, align=PP_ALIGN.RIGHT)
        rect(s, x + 0.28, yy + 0.31, 3.3, 0.01, fill=LINE, radius=0, shape=MSO_SHAPE.RECTANGLE)
        yy += 0.48
    x += 4.05

text(s, "One HTML file serves every screen. There is no separate mobile site.", 0.7, 5.7, 8.0, 0.35,
     size=11, italic=True, color=GREY)

rect(s, 0.62, 6.55, 12.1, 0.36, fill=GOLD, line=None, radius=0.3)
text(s, "Base CSS = phone  ·  @media (min-width: 768px) adds tablets  ·  @media (min-width: 1024px) adds desktops",
     0.9, 6.62, 11.6, 0.24, size=10.5, bold=True, color=DARK)
note(s, "We wrote the phone version first. The two media queries only add bigger layouts, they never fight the base "
        "styles. That is why the file has just two breakpoints. On a phone the navbar links wrap onto a second row, "
        "and every grid becomes one column, so nothing is ever squeezed.")

# ==================================================================
# 14. FORM SCRIPT
# ==================================================================
s = slide_new(LIGHT)
header(s, "The only JavaScript", "One script, one job: send the form", 14)
bullets(s, [
    ("The tag:", "<script src=\"js/form.js\"></script> before </body> in index.html only."),
    ("Today:", "form.js contains only a comment, as a placeholder."),
    ("Supplied by:", "the lecturer, who will replace the placeholder."),
    ("Reads:", "name attributes — fullname, phone, topic, message."),
    ("Does:", "stops the reload, validates, sends, shows a thank-you."),
    ("Gallery page:", "no script at all."),
], 0.7, 1.8, 6.9, 4.9, size=14)

rect(s, 7.95, 1.78, 4.8, 4.95, fill=DARK, line=DARK)
text(s, "LECTURER'S SCRIPT  ·  SIMPLIFIED", 8.2, 1.98, 4.3, 0.28, size=9.5, bold=True, color=GOLD)
code = ("const form =\n"
        "  document.querySelector(\n"
        "    '#contact-form');\n\n"
        "form.addEventListener(\n"
        "  'submit', function (e) {\n"
        "    e.preventDefault();\n\n"
        "    const name =\n"
        "      form.fullname.value;\n"
        "    const phone =\n"
        "      form.phone.value;\n"
        "    const topic =\n"
        "      form.topic.value;\n"
        "    const message =\n"
        "      form.message.value;\n\n"
        "    // send the data...\n"
        "  });")
text(s, code, 8.2, 2.4, 4.4, 4.1, size=9, color=RGBColor(0xD8, 0xE2, 0xF0), font="Consolas")
text(s, "CSS does the design. JavaScript only moves data.", 8.2, 6.35, 4.4, 0.3, size=9, italic=True,
     color=RGBColor(0x8D, 0x9E, 0xB6))
note(s, "We kept JavaScript to the absolute minimum required by the brief. The contact form needs a script to send "
        "data without reloading the page; that script comes from the lecturer. Our file is just a placeholder comment. "
        "Everything else on the site works with JavaScript switched off, which we demonstrated in testing.")

# ==================================================================
# 15. TESTING
# ==================================================================
s = slide_new()
header(s, "Testing", "What we checked before calling it finished", 15)
col1 = [
    ("Layout:", "no sideways scroll at 360, 768 or 1280px."),
    ("Media:", "30 images load, 16 videos play, none missing."),
    ("Links:", "every menu link works on both pages, including index.html#about."),
    ("Sections:", "every home section and both gallery grids present."),
]
col2 = [
    ("Accessibility:", "keyboard focus visible, labels linked, alt text on all images."),
    ("Performance:", "preload=metadata on every video, loading=lazy on the map."),
    ("Code rules:", "one stylesheet, no inline styles, no extra JavaScript."),
    ("Form:", "required fields block an empty submit."),
]
bullets(s, col1, 0.7, 1.82, 6.0, 2.6, size=13.5, gap=0.12)
bullets(s, col2, 6.9, 1.82, 6.0, 2.6, size=13.5, gap=0.12)

rect(s, 0.62, 5.95, 12.1, 0.85, fill=LIGHT, line=LINE)
text(s, "Result:", 0.9, 6.12, 1.2, 0.3, size=13, bold=True, color=NAVY)
text(s, "360px = 1 column   ·   768px = 2 columns   ·   1280px = 4 photo / 3 video columns   ·   0 broken links",
     2.0, 6.12, 10.4, 0.35, size=12, color=GREY)
text(s, "Checked in Chrome DevTools with the device toolbar and by resizing the window.", 0.9, 6.42, 9.0, 0.28,
     size=9.5, italic=True, color=GREY)

chips = [("0", "broken links"), ("30/30", "photos load"), ("16/16", "videos play"), ("3", "widths tested")]
cx = 0.7
for big, small in chips:
    rect(s, cx, 4.55, 2.85, 0.95, fill=WHITE, line=LINE)
    text(s, big, cx + 0.2, 4.66, 1.1, 0.45, size=20, bold=True, font=HEAD_FONT, color=NAVY)
    text(s, small, cx + 1.25, 4.82, 1.5, 0.3, size=10, color=GREY)
    cx += 3.0
note(s, "Testing was simple but thorough. We used the device toolbar to check 360, 768 and 1280 pixels, clicked every "
        "link, and confirmed that every media file loads. We also tested with the keyboard only: Tab reaches each "
        "field and the focus ring is clearly visible.")

# ==================================================================
# 16. TEAM ROLES
# ==================================================================
s = slide_new()
header(s, "Team", "Who did what", 16)

roles = [("Content & copy", "wrote every headline, paragraph and [EDIT] note"),
         ("Front-end", "index.html and gallery.html"),
         ("Styling", "css/style.css, hover effects and animations"),
         ("Media", "organised 30 photos and 16 videos, checked paths"),
         ("Docs & QA", "study guide, slides, testing at three widths")]
yy = 1.8
for role, task in roles:
    rect(s, 0.62, yy, 5.3, 0.62, fill=LIGHT, line=LINE, radius=0.1)
    text(s, role, 0.85, yy + 0.08, 2.2, 0.26, size=11, bold=True, color=NAVY)
    text(s, task, 0.85, yy + 0.33, 4.9, 0.24, size=8.8, color=GREY)
    yy += 0.74

rows, cols_n = 6, 4
tbl_shape = s.shapes.add_table(rows, cols_n, Inches(6.35), Inches(1.9), Inches(6.35), Inches(3.0))
table = tbl_shape.table
table.columns[0].width = Inches(1.75)
table.columns[1].width = Inches(1.75)
table.columns[2].width = Inches(1.55)
table.columns[3].width = Inches(1.3)
heads = ["Name [EDIT]", "Role", "Contribution %", "Signature"]
for r in range(rows):
    table.rows[r].height = Inches(0.5)
    for c in range(cols_n):
        cell = table.cell(r, c)
        cell.text = heads[c] if r == 0 else ""
        cell.margin_left = Inches(0.1)
        cell.margin_right = Inches(0.08)
        cell.margin_top = Inches(0.04)
        cell.margin_bottom = Inches(0.04)
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        cell.fill.solid()
        if r == 0:
            cell.fill.fore_color.rgb = NAVY
        else:
            cell.fill.fore_color.rgb = LIGHT if r % 2 else RGBColor(0xE9, 0xF0, 0xF9)
        p = cell.text_frame.paragraphs[0]
        p.font.size = Pt(9.5)
        p.font.bold = r == 0
        p.font.color.rgb = WHITE if r == 0 else NAVY
        p.font.name = BODY_FONT
text(s, "Fill the table with your real names before presenting.", 6.35, 5.35, 6.3, 0.3, size=10,
     italic=True, color=GREY)

rect(s, 0.62, 6.05, 12.1, 0.7, fill=LIGHT, line=LINE)
text(s, "5 roles   ·   1 shared folder   ·   4 weeks   ·   every member presents the part they built",
     0.95, 6.24, 11.5, 0.3, size=12, bold=True, color=NAVY)
note(s, "Here is how we divided the work. The table on the right is intentionally blank so each member can write "
        "their own name, role, percentage and signature before submission. Please fill it in and keep the total at 100 percent.")

# ==================================================================
# 17. Q&A
# ==================================================================
s = slide_new(NAVY)
rect(s, 0, 0, 0.18, 7.5, fill=GOLD, radius=0, shape=MSO_SHAPE.RECTANGLE)
text(s, "THANK YOU", 1.0, 1.55, 8.0, 0.4, size=13, bold=True, color=SKY)
text(s, "Questions?", 0.95, 2.0, 10.0, 1.2, size=64, bold=True, font=HEAD_FONT, color=WHITE)
rect(s, 1.0, 3.35, 2.2, 0.05, fill=GOLD, radius=0, shape=MSO_SHAPE.RECTANGLE)
text(s, "Swollen Sunday 2026  ·  First Love Church", 1.0, 3.65, 8.5, 0.4, size=16, color=RGBColor(0xD8, 0xE2, 0xF0))
text(s, "053 050 2572   ·   First Love Center, East Legon (Near UPSA), Accra", 1.0, 4.1, 9.5, 0.4,
     size=13, color=RGBColor(0x9F, 0xB1, 0xC9))
chip(s, "index.html", 1.0, 5.05, 2.2, fill=RGBColor(0x16, 0x2C, 0x51), color=WHITE)
chip(s, "gallery.html", 3.35, 5.05, 2.4, fill=RGBColor(0x16, 0x2C, 0x51), color=WHITE)
chip(s, "css/style.css", 5.9, 5.05, 2.45, fill=RGBColor(0x16, 0x2C, 0x51), color=WHITE)
chip(s, "js/form.js", 8.5, 5.05, 2.1, fill=RGBColor(0x16, 0x2C, 0x51), color=WHITE)
text(s, "Thank you for listening. We are happy to take questions on the design, the code or the testing.",
     1.0, 6.1, 10.5, 0.35, size=12, italic=True, color=RGBColor(0x8D, 0x9E, 0xB6))
note(s, "Thank you for listening. We are ready for questions. If you ask about a design choice, we will point to the "
        "client's need. If you ask about code, we will open the file and explain the exact rule.")

prs.save(OUT)
print("PPTX written:", OUT, "| slides:", len(prs.slides.__iter__.__self__._sldIdLst))
