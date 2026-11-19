"""Turn docs/CODE_EXPLANATION.md into a clean, printable PDF.

Run from the project root:
    python docs/make_pdf.py

Uses reportlab (pip install reportlab) and Segoe UI / Consolas from Windows.
"""

import os
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, Frame, HRFlowable, PageTemplate, Paragraph,
    Preformatted, Spacer, Table, TableStyle, KeepTogether,
)

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(BASE, "docs", "CODE_EXPLANATION.md")
OUT = os.path.join(BASE, "docs", "code_explanation.pdf")

NAVY = colors.HexColor("#0b1e3d")
GOLD = colors.HexColor("#b8860b")
GREY = colors.HexColor("#5b6b83")
CODE_BG = colors.HexColor("#f4f7fc")

# ---------------------------------------------------------------- fonts
FONTS = {
    "Body": (r"C:\Windows\Fonts\segoeui.ttf", r"C:\Windows\Fonts\segoeuib.ttf",
             r"C:\Windows\Fonts\segoeuii.ttf"),
    "Code": (r"C:\Windows\Fonts\consola.ttf", r"C:\Windows\Fonts\consolab.ttf",
             r"C:\Windows\Fonts\consolai.ttf"),
}
for name, paths in FONTS.items():
    if all(os.path.exists(p) for p in paths):
        pdfmetrics.registerFont(TTFont(name, paths[0]))
        pdfmetrics.registerFont(TTFont(name + "-Bold", paths[1]))
        pdfmetrics.registerFont(TTFont(name + "-Italic", paths[2]))
    else:  # fallback
        pdfmetrics.registerFont(TTFont(name, r"C:\Windows\Fonts\arial.ttf"))
        pdfmetrics.registerFont(TTFont(name + "-Bold", r"C:\Windows\Fonts\arialbd.ttf"))
        pdfmetrics.registerFont(TTFont(name + "-Italic", r"C:\Windows\Fonts\ariali.ttf"))

pdfmetrics.registerFontFamily("Code", normal="Code", bold="Code-Bold", italic="Code-Italic")
pdfmetrics.registerFontFamily("Body", normal="Body", bold="Body-Bold", italic="Body-Italic")

# ---------------------------------------------------------------- emoji filter
EMOJI = re.compile(
    "[" "\U0001F000-\U0001FAFF" "\u2600-\u27BF" "\uFE0F" "\u200D" "\u2B50" "\u2B06" "\u2B07" "]"
)


def clean(text):
    text = EMOJI.sub("", text)
    return text.replace("\u2011", "-")


# ---------------------------------------------------------------- styles
ss = getSampleStyleSheet()
title = ParagraphStyle("t", fontName="Body-Bold", fontSize=26, leading=31,
                       textColor=NAVY, spaceAfter=6)
subtitle = ParagraphStyle("st", fontName="Body", fontSize=10.5, leading=16,
                          textColor=GREY, spaceAfter=16)
h1 = ParagraphStyle("h1", fontName="Body-Bold", fontSize=19, leading=24,
                    textColor=NAVY, spaceBefore=22, spaceAfter=8)
h2 = ParagraphStyle("h2", fontName="Body-Bold", fontSize=13.5, leading=18,
                    textColor=NAVY, spaceBefore=18, spaceAfter=6)
h3 = ParagraphStyle("h3", fontName="Body-Bold", fontSize=11, leading=15,
                    textColor=GOLD, spaceBefore=12, spaceAfter=4)
body = ParagraphStyle("b", fontName="Body", fontSize=10, leading=15.5,
                      textColor=colors.HexColor("#1d2b3f"), spaceAfter=7,
                      alignment=TA_LEFT)
bullet = ParagraphStyle("bu", parent=body, leftIndent=16, bulletIndent=4,
                        spaceAfter=3)
code = ParagraphStyle("c", fontName="Code", fontSize=8.2, leading=11,
                      textColor=colors.HexColor("#22303f"), backColor=CODE_BG,
                      borderPadding=7, spaceBefore=3, spaceAfter=10,
                      leftIndent=2, rightIndent=2)
cell = ParagraphStyle("cell", fontName="Body", fontSize=8.6, leading=11.5,
                      textColor=colors.HexColor("#1d2b3f"))
cell_head = ParagraphStyle("cellh", parent=cell, fontName="Body-Bold",
                           textColor=colors.white)

# ---------------------------------------------------------------- inline markdown
def inline(text):
    text = clean(text)
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<i>\1</i>", text)
    text = re.sub(r"`(.+?)`", r'<font name="Code" size="8.6" color="#9b2c2c">\1</font>', text)
    return text


def make_table(rows):
    ncols = max(len(r) for r in rows)
    rows = [r + [""] * (ncols - len(r)) for r in rows]
    data = []
    for i, row in enumerate(rows):
        style = cell_head if i == 0 else cell
        data.append([Paragraph(inline(c), style) for c in row])
    width = 495
    first = 110 if ncols == 2 else (95 if ncols == 3 else width / ncols)
    rest = (width - first) / (ncols - 1) if ncols > 1 else width
    widths = [first] + [rest] * (ncols - 1)
    table = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#d5deea")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f7f9fc")]),
    ]))
    return table


# ---------------------------------------------------------------- parse markdown
lines = open(MD, encoding="utf-8").read().splitlines()
story = []
i = 0
first_heading = True

while i < len(lines):
    line = lines[i].rstrip()

    if not line.strip():
        i += 1
        continue

    # fenced code
    if line.strip().startswith("```"):
        i += 1
        block = []
        while i < len(lines) and not lines[i].strip().startswith("```"):
            block.append(clean(lines[i]).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
            i += 1
        i += 1
        story.append(Preformatted("\n".join(block), code))
        continue

    # table
    if line.strip().startswith("|"):
        rows = []
        while i < len(lines) and lines[i].strip().startswith("|"):
            raw = lines[i].strip().strip("|")
            if not re.match(r"^[\s|:-]+$", raw):
                rows.append([c.strip() for c in raw.split("|")])
            i += 1
        if rows:
            story.append(Spacer(1, 2))
            story.append(make_table(rows))
            story.append(Spacer(1, 10))
        continue

    # horizontal rule
    if line.strip() == "---":
        story.append(Spacer(1, 4))
        story.append(HRFlowable(width="100%", thickness=0.7, color=colors.HexColor("#d5deea")))
        story.append(Spacer(1, 8))
        i += 1
        continue

    # headings
    if line.startswith("### "):
        story.append(Paragraph(inline(line[4:]), h3))
        i += 1
        continue
    if line.startswith("## "):
        story.append(Paragraph(inline(line[3:]), h2))
        i += 1
        continue
    if line.startswith("# "):
        story.append(Paragraph(inline(line[2:]), title if first_heading else h1))
        first_heading = False
        i += 1
        continue

    # bullets
    if line.lstrip().startswith("- "):
        text = line.lstrip()[2:]
        story.append(Paragraph(inline(text), bullet, bulletText="\u2022"))
        i += 1
        continue

    # numbered list
    m = re.match(r"^(\d+)\.\s+(.*)$", line.strip())
    if m:
        story.append(Paragraph(inline(m.group(2)), bullet, bulletText=m.group(1) + "."))
        i += 1
        continue

    # paragraph (gather wrapped lines)
    para = [line.strip()]
    i += 1
    while i < len(lines):
        nxt = lines[i].strip()
        if (not nxt or nxt.startswith(("#", "|", "```", "- ", "---"))
                or re.match(r"^\d+\.\s", nxt)):
            break
        para.append(nxt)
        i += 1
    story.append(Paragraph(inline(" ".join(para)), body))

# ---------------------------------------------------------------- document
doc = BaseDocTemplate(OUT, pagesize=A4,
                      leftMargin=50, rightMargin=50, topMargin=54, bottomMargin=48,
                      title="Swollen Sunday 2026 - Code Explanation",
                      author="Swollen Sunday 2026 project team")

frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="main")


def decorate(canvas, doc_obj):
    canvas.saveState()
    canvas.setFont("Body", 7.5)
    canvas.setFillColor(GREY)
    canvas.drawString(50, A4[1] - 32, "SWOLLEN SUNDAY 2026  |  CODE EXPLANATION")
    canvas.setStrokeColor(colors.HexColor("#d5deea"))
    canvas.setLineWidth(0.6)
    canvas.line(50, A4[1] - 38, A4[0] - 50, A4[1] - 38)
    canvas.drawRightString(A4[0] - 50, 26, "Page %d" % doc_obj.page)
    canvas.drawString(50, 26, "First Love Church  -  HTML & CSS study guide")
    canvas.restoreState()


doc.addPageTemplates([PageTemplate(id="page", frames=[frame], onPage=decorate)])
doc.build(story)
print("PDF written:", OUT)
