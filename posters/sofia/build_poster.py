#!/usr/bin/env python3
# Electric Vernacular  -  "THIS IS SOFIA."  birth poster
import math
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FONTS = "/root/.claude/skills/canvas-design/canvas-fonts/"
OUT   = "/home/user/website/posters/sofia/sofia-durazzo-poster.pdf"

# ---------- palette ----------
BLUE   = HexColor("#141C8C")   # deep royal cobalt field
BLUE_D = HexColor("#101672")   # deeper for vignette
MAGENTA= HexColor("#FF2E7E")   # hot magenta spark
ROSE   = HexColor("#F5B9CB")   # soft rose echo
CREAM  = HexColor("#F5F1E8")   # warm gallery white
CREAM2 = HexColor("#EAE4D6")

# ---------- page ----------
W, H = 1296.0, 1728.0          # 18 x 24 in
ML   = 108.0                   # left margin
MR   = 108.0
MT   = 104.0
MB   = 104.0

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
    """largest size so tracked width <= target_w"""
    size = start
    while size > 8:
        if tw(s, font, size, track_ratio*size) <= target_w:
            return size
        size -= 0.5
    return size

# =====================================================================
# FIELD  (royal blue with a soft radial vignette toward the sun)
# =====================================================================
c.setFillColor(BLUE); c.rect(0, 0, W, H, fill=1, stroke=0)

# subtle vignette: darker rings toward corners, drawn as faint bands
sun_x, sun_y = 946.0, 1236.0
c.saveState()
for i in range(60):
    r = 1500 - i*22
    a = 0.010
    c.setFillColor(BLUE_D); c.setFillAlpha(a)
    c.circle(sun_x, sun_y, r, fill=1, stroke=0)
c.restoreState()

# =====================================================================
# THE SUN  (Leo / July radiance)  -  meticulous field of fine rays
# =====================================================================
c.saveState()
N = 96
r_in  = 74.0
for k in range(N):
    ang = (2*math.pi*k)/N
    # alternate long/short rays for rhythm
    long = (k % 2 == 0)
    r_out = (300.0 if long else 210.0)
    x1 = sun_x + r_in*math.cos(ang); y1 = sun_y + r_in*math.sin(ang)
    x2 = sun_x + r_out*math.cos(ang); y2 = sun_y + r_out*math.sin(ang)
    c.setStrokeColor(ROSE if long else MAGENTA)
    c.setStrokeAlpha(0.55 if long else 0.35)
    c.setLineWidth(1.15 if long else 0.9)
    c.setLineCap(1)
    c.line(x1, y1, x2, y2)
# inner disc rings
c.setStrokeColor(ROSE); c.setStrokeAlpha(0.85); c.setLineWidth(1.4)
c.circle(sun_x, sun_y, r_in, fill=0, stroke=1)
c.setStrokeAlpha(0.45); c.setLineWidth(1.0)
c.circle(sun_x, sun_y, r_in-11, fill=0, stroke=1)
# solid magenta core dot
c.setFillColor(MAGENTA); c.setFillAlpha(1.0)
c.circle(sun_x, sun_y, 8.5, fill=1, stroke=0)
c.restoreState()

# =====================================================================
# TOP MICRO-HEADER  (instrument-panel marginalia)
# =====================================================================
top = H - MT
c.setStrokeColor(CREAM); c.setStrokeAlpha(0.9); c.setLineWidth(1.2)
c.line(ML, top, W-MR, top)
text(ML, top+11, "BIRTH  ANNOUNCEMENT", "Mono", 12.5, CREAM, track=4.6, alpha=0.92)
text(W-MR, top+11, "Nº 001", "Mono", 12.5, ROSE, track=4.6, align="right")
# small registration crosses just under the rule
def cross(x, y, s, col, w=1.0, a=0.9):
    c.saveState(); c.setStrokeColor(col); c.setStrokeAlpha(a); c.setLineWidth(w)
    c.line(x-s, y, x+s, y); c.line(x, y-s, x, y+s); c.restoreState()
cross(ML+4, top-26, 5, ROSE)
cross(W-MR-4, top-26, 5, ROSE)

# =====================================================================
# LEFT-MARGIN VERTICAL CAPTION  (editorial spine detail)
# =====================================================================
c.saveState()
c.translate(62, 1112)
c.rotate(90)
text(0, 0, "THE THIRTY·FIRST OF JULY · MMXXVI", "Mono", 11, CREAM, track=3.4, alpha=0.55)
c.restoreState()

# =====================================================================
# HERO TYPE STACK
# =====================================================================
content_w = W - ML - MR

# "THIS IS", tracked display, rose
text(ML, 1006, "THIS  IS", "Disp", 118, ROSE, track=6)

# "SOFIA", giant condensed, leaving room for the slash sign-off
base = 636.0
sofia_size = fit_size("SOFIA", "Disp", content_w-232, track_ratio=0.0, start=460)
sofia_w = tw("SOFIA", "Disp", sofia_size, 0)
cap = sofia_size*0.715          # measured cap height of Big Shoulders
text(ML, base, "SOFIA", "Disp", sofia_size, CREAM, track=0)

# the signature SLASH (parallelogram) breaking the grid, SOFIA // sign-off
def parallelogram(x, y, w, h, skew, color, alpha=1.0):
    c.saveState(); c.setFillColor(color); c.setFillAlpha(alpha)
    p = c.beginPath()
    p.moveTo(x, y); p.lineTo(x+w, y); p.lineTo(x+w+skew, y+h); p.lineTo(x+skew, y+h)
    p.close(); c.drawPath(p, fill=1, stroke=0); c.restoreState()

# aligned to the cap of SOFIA, sitting just after the final "A"
sx = ML + sofia_w + 40
skew = cap*0.34
parallelogram(sx,      base, 60, cap, skew, MAGENTA, 1.0)
parallelogram(sx+86,   base, 28, cap, skew, ROSE, 0.9)

# "DURAZZO", tracked, cream, sits below SOFIA
dz_size = 132
# fit durazzo to width if needed
dz_size = min(dz_size, fit_size("DURAZZO", "DispR", content_w, track_ratio=0.14, start=140))
text(ML, 512, "DURAZZO", "DispR", dz_size, CREAM2, track=dz_size*0.14)

# thin rule under name block
c.setStrokeColor(CREAM); c.setStrokeAlpha(0.35); c.setLineWidth(1.0)
c.line(ML, 476, W-MR, 476)

# =====================================================================
# TONE TRIAD  (homage to "ELLA IS HUMAN / FEMALE / YOUNG")
# =====================================================================
triad = [("SOFIA IS ", "NEW."), ("SOFIA IS ", "BRIGHT."), ("SOFIA IS ", "HERE.")]
ty = 408
for a, b in triad:
    x = ML
    wa = text(x, ty, a, "SansB", 25, CREAM, track=3.2, alpha=0.92)
    text(x+wa, ty, b, "SansB", 25, MAGENTA, track=3.2)
    ty -= 46

# =====================================================================
# FOOTER  (clinical date coordinates)
# =====================================================================
foot = MB + 40
c.setStrokeColor(CREAM); c.setStrokeAlpha(0.9); c.setLineWidth(1.2)
c.line(ML, foot, W-MR, foot)
# fine measurement ticks along the rule (instrument-panel precision)
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
text(W/2, foot-30, "A  GIRL", "Mono", 13.5, ROSE, track=4.4, align="center")
leo_w = tw("LEO", "Mono", 13.5, 4.4)
text(W-MR, foot-30, "LEO", "Mono", 13.5, CREAM, track=4.4, align="right", alpha=0.95)
mini_sun(W-MR-leo_w-16, foot-25.5, 8, ROSE, 0.95)
cross(ML+4, foot+22, 5, ROSE)
cross(W-MR-4, foot+22, 5, ROSE)

c.showPage()
c.save()
print("wrote", OUT)
