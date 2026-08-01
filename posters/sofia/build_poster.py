#!/usr/bin/env python3
# Electric Vernacular, "THIS IS SOFIA." birth poster
# Palette: mid-century arena, warm cream mat, deep navy field, brick-red pop.
import math
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FONTS = "/root/.claude/skills/canvas-design/canvas-fonts/"
OUT   = "/home/user/website/posters/sofia/sofia-durazzo-poster.pdf"

# ---------- palette ----------
NAVY   = HexColor("#1B2A57")   # deep royal navy field
NAVY_D = HexColor("#141F42")   # deeper navy, vignette
RED    = HexColor("#D23A66")   # raspberry magenta-pink pop
CREAM  = HexColor("#ECE3CD")   # warm oatmeal (type on navy)
CREAM2 = HexColor("#D8CDB0")
BORDER = HexColor("#F0EAD9")   # warm off-white mat

# ---------- page ----------
W, H = 1296.0, 1728.0          # 18 x 24 in
B    = 74.0                    # cream mat / border width
ML   = 122.0                   # content left  (inside the mat)
MR   = 122.0
MT   = 118.0
MB   = 118.0

# ---------- fonts ----------
pdfmetrics.registerFont(TTFont("Disp",  FONTS+"BigShoulders-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DispR", FONTS+"BigShoulders-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Sans",  FONTS+"Outfit-Regular.ttf"))
pdfmetrics.registerFont(TTFont("SansB", FONTS+"Outfit-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Mono",  FONTS+"GeistMono-Regular.ttf"))

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

# =====================================================================
# FIELD
# =====================================================================
c.setFillColor(NAVY); c.rect(0, 0, W, H, fill=1, stroke=0)

# subtle vignette toward the sun
sun_x, sun_y = 902.0, 1240.0
c.saveState()
for i in range(60):
    r = 1500 - i*22
    c.setFillColor(NAVY_D); c.setFillAlpha(0.010)
    c.circle(sun_x, sun_y, r, fill=1, stroke=0)
c.restoreState()

# =====================================================================
# THE SUN  (Leo / July radiance)
# =====================================================================
c.saveState()
N = 96
r_in  = 72.0
for k in range(N):
    ang = (2*math.pi*k)/N
    long = (k % 2 == 0)
    r_out = (288.0 if long else 205.0)
    x1 = sun_x + r_in*math.cos(ang); y1 = sun_y + r_in*math.sin(ang)
    x2 = sun_x + r_out*math.cos(ang); y2 = sun_y + r_out*math.sin(ang)
    c.setStrokeColor(CREAM if long else RED)
    c.setStrokeAlpha(0.50 if long else 0.42)
    c.setLineWidth(1.15 if long else 0.9)
    c.setLineCap(1)
    c.line(x1, y1, x2, y2)
c.setStrokeColor(CREAM); c.setStrokeAlpha(0.85); c.setLineWidth(1.4)
c.circle(sun_x, sun_y, r_in, fill=0, stroke=1)
c.setStrokeAlpha(0.42); c.setLineWidth(1.0)
c.circle(sun_x, sun_y, r_in-11, fill=0, stroke=1)
c.setFillColor(RED); c.setFillAlpha(1.0)
c.circle(sun_x, sun_y, 8.5, fill=1, stroke=0)
c.restoreState()

# =====================================================================
# TOP MICRO-HEADER
# =====================================================================
top = H - MT
c.setStrokeColor(CREAM); c.setStrokeAlpha(0.9); c.setLineWidth(1.2)
c.line(ML, top, W-MR, top)
text(ML, top+11, "BIRTH  ANNOUNCEMENT", "Mono", 12.5, CREAM, track=4.6, alpha=0.92)

# navy+red flag mark, top-right corner  (arena-poster signature)
def flag(x, y, w, h, sk):
    def half(x0, w0, col):
        c.saveState(); c.setFillColor(col); c.setFillAlpha(1.0)
        p = c.beginPath()
        p.moveTo(x0, y); p.lineTo(x0+w0, y); p.lineTo(x0+w0+sk, y+h); p.lineTo(x0+sk, y+h)
        p.close(); c.drawPath(p, fill=1, stroke=0); c.restoreState()
    half(x,        w/2, RED)
    half(x+w/2,    w/2, CREAM)
_fw, _fh, _fsk = 50.0, 24.0, 12.0
flag(W-MR-_fw-_fsk, top+9, _fw, _fh, _fsk)
def cross(x, y, s, col, w=1.0, a=0.9):
    c.saveState(); c.setStrokeColor(col); c.setStrokeAlpha(a); c.setLineWidth(w)
    c.line(x-s, y, x+s, y); c.line(x, y-s, x, y+s); c.restoreState()
cross(ML+4, top-26, 5, RED)
cross(W-MR-4, top-26, 5, RED)

# =====================================================================
# LEFT-MARGIN VERTICAL CAPTION
# =====================================================================
c.saveState()
c.translate(102, 1108)
c.rotate(90)
text(0, 0, "THE THIRTY·FIRST OF JULY · MMXXVI", "Mono", 11, CREAM, track=3.4, alpha=0.55)
c.restoreState()

# =====================================================================
# HERO TYPE STACK
# =====================================================================
content_w = W - ML - MR

text(ML, 1006, "THIS  IS", "Disp", 118, RED, track=6)

base = 636.0
sofia_size = fit_size("SOFIA", "Disp", content_w-232, track_ratio=0.0, start=460)
sofia_w = tw("SOFIA", "Disp", sofia_size, 0)
cap = sofia_size*0.715
text(ML, base, "SOFIA", "Disp", sofia_size, CREAM, track=0)

def parallelogram(x, y, w, h, skew, color, alpha=1.0):
    c.saveState(); c.setFillColor(color); c.setFillAlpha(alpha)
    p = c.beginPath()
    p.moveTo(x, y); p.lineTo(x+w, y); p.lineTo(x+w+skew, y+h); p.lineTo(x+skew, y+h)
    p.close(); c.drawPath(p, fill=1, stroke=0); c.restoreState()

sx = ML + sofia_w + 40
skew = cap*0.34
parallelogram(sx,    base, 60, cap, skew, RED, 1.0)
parallelogram(sx+86, base, 28, cap, skew, CREAM, 0.92)

dz_size = min(132, fit_size("DURAZZO", "DispR", content_w, track_ratio=0.14, start=140))
text(ML, 512, "DURAZZO", "DispR", dz_size, CREAM2, track=dz_size*0.14)

c.setStrokeColor(CREAM); c.setStrokeAlpha(0.35); c.setLineWidth(1.0)
c.line(ML, 476, W-MR, 476)

# =====================================================================
# FOOTER  (clinical date coordinates)
# =====================================================================
foot = MB + 40
c.setStrokeColor(CREAM); c.setStrokeAlpha(0.9); c.setLineWidth(1.2)
c.line(ML, foot, W-MR, foot)
c.saveState(); c.setStrokeColor(CREAM); c.setStrokeAlpha(0.45); c.setLineWidth(0.8)
span = (W-MR) - ML
for i in range(41):
    x = ML + span*i/40.0
    tick = 9 if i % 5 == 0 else 5
    c.line(x, foot, x, foot+tick)
c.restoreState()

def mini_sun(cx, cy, R, col, alpha=1.0):
    c.saveState(); c.setStrokeColor(col); c.setFillColor(col)
    c.setStrokeAlpha(alpha); c.setFillAlpha(alpha); c.setLineWidth(1.1); c.setLineCap(1)
    c.circle(cx, cy, R*0.52, fill=1, stroke=0)
    for k in range(8):
        a = math.pi*k/4
        c.line(cx+R*0.78*math.cos(a), cy+R*0.78*math.sin(a),
               cx+R*1.15*math.cos(a), cy+R*1.15*math.sin(a))
    c.restoreState()

text(ML, foot-30, "EST. 07 · 31 · 2026", "Mono", 13.5, CREAM, track=3.2, alpha=0.95)
text(W/2, foot-30, "A  GIRL", "Mono", 13.5, RED, track=4.4, align="center")
leo_w = tw("LEO", "Mono", 13.5, 4.4)
text(W-MR, foot-30, "LEO", "Mono", 13.5, CREAM, track=4.4, align="right", alpha=0.95)
mini_sun(W-MR-leo_w-16, foot-25.5, 8, RED, 0.95)

# =====================================================================
# CREAM MAT / BORDER  (drawn last to crop the field to a clean window)
# =====================================================================
c.setFillColor(BORDER)
c.rect(0, 0, B, H, fill=1, stroke=0)            # left
c.rect(W-B, 0, B, H, fill=1, stroke=0)          # right
c.rect(0, 0, W, B, fill=1, stroke=0)            # bottom
c.rect(0, H-B, W, B, fill=1, stroke=0)          # top
# thin red keyline at the field boundary
c.setStrokeColor(RED); c.setStrokeAlpha(0.9); c.setLineWidth(1.4)
c.rect(B, B, W-2*B, H-2*B, fill=0, stroke=1)

c.showPage()
c.save()
print("wrote", OUT)
