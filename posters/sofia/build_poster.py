#!/usr/bin/env python3
# "SOFIA DURAZZO" birth poster, playful-editorial (Vicki Tan book-cover language):
# warm blush ground, cobalt-royal blue, sunny yellow, black ink, arched bold
# type, a rising-sun illustration, a serif line, tracked caps, yellow spine.
import math
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FONTS = "/root/.claude/skills/canvas-design/canvas-fonts/"
OUT   = "/home/user/website/posters/sofia/sofia-durazzo-poster.pdf"

# ---------- palette ----------
BLUSH  = HexColor("#F3E5DF")   # warm blush ground
BLUE   = HexColor("#2B43D6")   # cobalt royal blue
BLUE_D = HexColor("#20308F")   # deeper blue (shadows)
YELLOW = HexColor("#F4C21B")   # sunny yellow pop
INK    = HexColor("#1C1B1A")   # soft black

# ---------- page ----------
W, H = 1296.0, 1728.0
STRIPE = 46.0                  # yellow spine width
ML = STRIPE + 118.0
MR = 118.0
MB = 120.0
cx = STRIPE + (W - STRIPE)/2.0 # optical center of the content field

# ---------- fonts ----------
pdfmetrics.registerFont(TTFont("Grot",  FONTS+"WorkSans-Bold.ttf"))       # arch + caps
pdfmetrics.registerFont(TTFont("GrotR", FONTS+"WorkSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Serif", FONTS+"LibreBaskerville-Regular.ttf"))  # subtitle

c = canvas.Canvas(OUT, pagesize=(W, H))

def sw(s, font, size, track=0.0):
    return pdfmetrics.stringWidth(s, font, size) + track*max(0, len(s)-1)

def text(x, y, s, font, size, color, track=0.0, align="left", alpha=1.0):
    width = sw(s, font, size, track)
    if   align == "center": x -= width/2.0
    elif align == "right":  x -= width
    c.saveState(); c.setFillColor(color); c.setFillAlpha(alpha)
    t = c.beginText(); t.setTextOrigin(x, y); t.setFont(font, size); t.setCharSpace(track)
    t.textOut(s); c.drawText(t); c.restoreState()
    return width

def arch_text(ccx, ccy, R, s, font, size, color, track=0.0):
    """set string s along the top of a circle (radius R, center ccx,ccy)."""
    adv = [pdfmetrics.stringWidth(ch, font, size) + track for ch in s]
    span = sum(adv)/R
    ang = math.pi/2 + span/2.0
    for ch, w in zip(s, adv):
        a = ang - (w/2.0)/R
        gx = ccx + R*math.cos(a); gy = ccy + R*math.sin(a)
        c.saveState(); c.setFillColor(color)
        c.translate(gx, gy); c.rotate(math.degrees(a - math.pi/2))
        cw = pdfmetrics.stringWidth(ch, font, size)
        t = c.beginText(); t.setTextOrigin(-cw/2.0, 0); t.setFont(font, size); t.textOut(ch)
        c.drawText(t); c.restoreState()
        ang -= w/R

def star(px, py, r, color, alpha=1.0, points=5, rot=-math.pi/2):
    c.saveState(); c.setFillColor(color); c.setFillAlpha(alpha)
    p = c.beginPath(); inner = r*0.42
    for i in range(points*2):
        rr = r if i % 2 == 0 else inner
        a = rot + math.pi*i/points
        xx = px + rr*math.cos(a); yy = py + rr*math.sin(a)
        (p.moveTo if i == 0 else p.lineTo)(xx, yy)
    p.close(); c.drawPath(p, fill=1, stroke=0); c.restoreState()

# =====================================================================
# GROUND + yellow spine
# =====================================================================
c.setFillColor(BLUSH); c.rect(0, 0, W, H, fill=1, stroke=0)
c.setFillColor(YELLOW); c.rect(0, 0, STRIPE, H, fill=1, stroke=0)

# =====================================================================
# RISING SUN  (dawn / July / Leo)  -  the flat playful illustration
# =====================================================================
HZ = 700.0          # horizon line
Rs = 162.0          # sun radius
# soft yellow halo
c.saveState(); c.setFillColor(YELLOW); c.setFillAlpha(0.42)
c.circle(cx, HZ, Rs*1.7, fill=1, stroke=0); c.restoreState()
# tapered rays (upper half only, masked below)
c.saveState()
NR = 18
for k in range(NR+1):
    a = math.pi * k/NR          # 0..pi  (above horizon)
    r0 = Rs*1.16; r1 = Rs*1.72
    half = 0.028
    x1 = cx + r0*math.cos(a-half); y1 = HZ + r0*math.sin(a-half)
    x2 = cx + r0*math.cos(a+half); y2 = HZ + r0*math.sin(a+half)
    xt = cx + r1*math.cos(a);       yt = HZ + r1*math.sin(a)
    p = c.beginPath(); p.moveTo(x1,y1); p.lineTo(xt,yt); p.lineTo(x2,y2); p.close()
    c.setFillColor(BLUE); c.drawPath(p, fill=1, stroke=0)
c.restoreState()
# sun disk
c.setFillColor(BLUE); c.circle(cx, HZ, Rs, fill=1, stroke=0)
# a couple of stars in the sky
star(cx-244, HZ+250, 15, BLUE, 1.0)
star(cx+250, HZ+300, 11, YELLOW, 1.0)
star(cx+238, HZ+120, 9,  INK,  1.0)
star(cx-238, HZ+120, 7,  INK,  1.0)
# mask everything below the horizon for a clean rising sun
c.setFillColor(BLUSH); c.rect(0, 0, W, HZ, fill=1, stroke=0)
c.setFillColor(YELLOW); c.rect(0, 0, STRIPE, HZ, fill=1, stroke=0)
# horizon rule
c.setStrokeColor(INK); c.setLineWidth(2.2); c.line(ML, HZ, W-MR, HZ)

# =====================================================================
# ARCHED NAME  (the "title")
# =====================================================================
arch_cy = 748.0
arch_R  = 596.0
name_size = 160
# fit so the name spans a generous arch without crowding the edges
while sw("SOFIA DURAZZO", "Grot", name_size, 6)/arch_R > 2.80 and name_size > 40:
    name_size -= 1
arch_text(cx, arch_cy, arch_R, "SOFIA DURAZZO", "Grot", name_size, INK, track=6)

# =====================================================================
# SERIF SUBTITLE + DATE  (the "author" line sits in the lower third)
# =====================================================================
text(cx, 610, "A Brand-New Human, Here to Discover", "Serif", 30, INK, align="center")
text(cx, 562, "Life’s Big and Little Wonders",       "Serif", 30, INK, align="center")

text(cx, 384, "BORN THE 31ST OF JULY  ·  2026", "Grot", 22, BLUE, track=3.4, align="center")
text(cx, 338, "A  BIRTH  ANNOUNCEMENT", "GrotR", 12.5, INK, track=5.2, align="center", alpha=0.68)

c.showPage()
c.save()
print("wrote", OUT)
