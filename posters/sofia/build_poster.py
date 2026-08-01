#!/usr/bin/env python3
# Electric Vernacular (restrained), "THIS IS SOFIA." birth poster
# Faithful to the Ella brand language: thin condensed type, one clean
# parallelogram gesture, deep royal navy + soft mauve-rose, generous space.
import math
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FONTS = "/root/.claude/skills/canvas-design/canvas-fonts/"
OUT   = "/home/user/website/posters/sofia/sofia-durazzo-poster.pdf"

# ---------- palette ----------
BLUE   = HexColor("#16295F")   # deep royal navy field
MAUVE  = HexColor("#DBACB4")   # soft rose-mauve (the Ella accent)
MAUVE_D= HexColor("#CF9DA6")   # slightly deeper mauve
ROSE_T = HexColor("#E7C6CC")   # pale rose for micro labels
CREAM  = HexColor("#F2EEE4")   # warm gallery white
CREAM2 = HexColor("#E4DECF")

# ---------- page ----------
W, H = 1296.0, 1728.0          # 18 x 24 in
ML   = 122.0                   # margins, generous
MR   = 122.0
MT   = 120.0
MB   = 120.0

# ---------- fonts ----------
pdfmetrics.registerFont(TTFont("Disp",  FONTS+"BigShoulders-Regular.ttf"))  # thin condensed hero
pdfmetrics.registerFont(TTFont("DispB", FONTS+"BigShoulders-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Sans",  FONTS+"Outfit-Regular.ttf"))        # Sofia Pro stand-in
pdfmetrics.registerFont(TTFont("SansB", FONTS+"Outfit-Bold.ttf"))

c = canvas.Canvas(OUT, pagesize=(W, H))

def tw(text, font, size, track=0.0):
    return pdfmetrics.stringWidth(text, font, size) + track*max(0, len(text)-1)

def text(x, y, s, font, size, color, track=0.0, align="left", alpha=1.0):
    width = tw(s, font, size, track)
    if   align == "center": x -= width/2.0
    elif align == "right":  x -= width
    c.saveState()
    c.setFillColor(color); c.setFillAlpha(alpha)
    t = c.beginText(); t.setTextOrigin(x, y)
    t.setFont(font, size); t.setCharSpace(track)
    t.textOut(s)
    c.drawText(t)
    c.restoreState()
    return width

def fit_size(s, font, target_w, track_ratio=0.0, start=400):
    size = start
    while size > 8:
        if tw(s, font, size, track_ratio*size) <= target_w:
            return size
        size -= 0.5
    return size

def parallelogram(x, y, w, h, skew, color, alpha=1.0, stroke=False, lw=2.0):
    c.saveState()
    c.setFillColor(color); c.setFillAlpha(alpha)
    c.setStrokeColor(color); c.setStrokeAlpha(alpha); c.setLineWidth(lw)
    p = c.beginPath()
    p.moveTo(x, y); p.lineTo(x+w, y); p.lineTo(x+w+skew, y+h); p.lineTo(x+skew, y+h)
    p.close()
    c.drawPath(p, fill=(0 if stroke else 1), stroke=(1 if stroke else 0))
    c.restoreState()

# =====================================================================
# FIELD
# =====================================================================
c.setFillColor(BLUE); c.rect(0, 0, W, H, fill=1, stroke=0)

# =====================================================================
# THE GESTURE, a tall mauve parallelogram on the right (Ella cover),
# with a slim cream companion, two-tone like the Ella decoration page.
# =====================================================================
parallelogram(918, 806, 190, 612, 176, MAUVE, 1.0)          # main slab
parallelogram(884, 806, 20, 612, 176, CREAM, 1.0)           # crisp cream keyline

# =====================================================================
# TOP MICRO-HEADER
# =====================================================================
top = H - MT
text(ML, top, "BIRTH  ANNOUNCEMENT", "Sans", 13, ROSE_T, track=5.2, alpha=0.95)
text(W-MR, top, "Nº 001", "Sans", 13, ROSE_T, track=5.2, align="right", alpha=0.95)
c.setStrokeColor(CREAM); c.setStrokeAlpha(0.35); c.setLineWidth(1.0)
c.line(ML, top-18, W-MR, top-18)

# =====================================================================
# HERO STATEMENT, thin condensed, tracked, stacked  (left column)
# =====================================================================
col_w = 780  # left type column, keeps clear of the slab

# "THIS IS"
text(ML, 1214, "THIS IS", "Disp", 92, ROSE_T, track=8)

# "SOFIA", the hero, thin and large but composed
sofia_size = fit_size("SOFIA", "Disp", col_w, track_ratio=0.02, start=300)
text(ML, 966, "SOFIA", "Disp", sofia_size, CREAM, track=sofia_size*0.02)

# "DURAZZO."
dz_size = fit_size("DURAZZO.", "Disp", col_w, track_ratio=0.06, start=150)
dz_size = min(dz_size, 132)
text(ML, 838, "DURAZZO.", "Disp", dz_size, CREAM, track=dz_size*0.06)

# established micro-caps beneath the name (Ella "ESTABLISHED ..." device)
text(ML, 788, "ESTABLISHED 07 · 31 · 2026  |  LEO  |  MMXXVI",
     "Sans", 12.5, ROSE_T, track=3.4, alpha=0.9)

# =====================================================================
# TONE TRIAD, restrained homage, lower-left
# =====================================================================
c.setStrokeColor(CREAM); c.setStrokeAlpha(0.30); c.setLineWidth(1.0)
c.line(ML, 360, ML+300, 360)
text(ML, 322, "BRAND TONE", "Sans", 11, ROSE_T, track=4.2, alpha=0.85)

triad = [("SOFIA IS ", "NEW."), ("SOFIA IS ", "BRIGHT."), ("SOFIA IS ", "HERE.")]
ty = 268
for a, b in triad:
    wa = text(ML, ty, a, "Disp", 44, CREAM, track=2.4)
    text(ML+wa, ty, b, "Disp", 44, MAUVE, track=2.4)
    ty -= 58

# small parallelogram echo, lower-right, to balance the triad
parallelogram(1052, 236, 58, 150, 43, MAUVE, 1.0)
parallelogram(1036, 236, 8, 150, 43, CREAM, 1.0)

# =====================================================================
# FOOTER
# =====================================================================
foot = MB - 8
c.setStrokeColor(CREAM); c.setStrokeAlpha(0.35); c.setLineWidth(1.0)
c.line(ML, foot+22, W-MR, foot+22)
text(ML, foot-8, "SOFIA DURAZZO", "Sans", 12, CREAM, track=4.0, alpha=0.9)
text(W-MR, foot-8, "A GIRL", "Sans", 12, ROSE_T, track=4.6, align="right", alpha=0.95)

c.showPage()
c.save()
print("wrote", OUT)
