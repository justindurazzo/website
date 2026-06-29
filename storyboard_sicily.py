from PIL import Image, ImageDraw, ImageFont, ImageOps

BASE = "/root/.claude/uploads/f650b114-7abe-53e3-98ba-153e056e5d84/"

CHAPTERS = [
    ("CH.1  BUONGIORNO, PALERMO", [
        ("61aa4aed-IMG_5899.jpeg", "1 you/street",    0.50, 0.45),
        ("ba697cea-IMG_5836.jpeg", "2 tabacchi",      0.50, 0.50),
        ("e56a5853-IMG_5813.jpeg", "3 balcony",       0.50, 0.50),
        ("36b629d6-IMG_6065.jpeg", "4 horse",         0.50, 0.45),
        ("f5ffbb44-IMG_5860.jpeg", "5 antiques",      0.50, 0.45),
    ]),
    ("CH.2  AL MERCATO", [
        ("4c780564-IMG_6026.jpeg", "6 seafood",       0.50, 0.50),
        ("f4a22a6d-IMG_6034.jpeg", "7 olives",        0.50, 0.45),
        ("f07c6889-IMG_6090.jpeg", "8 madonna",       0.50, 0.50),
        ("ca74efdf-IMG_6047.jpeg", "9 porchetta",     0.50, 0.45),
        ("253e6871-IMG_5871.jpeg", "10 you/mirror",   0.50, 0.50),
    ]),
    ("CH.3  MANGIA", [
        ("8fffc94a-IMG_6070.jpeg", "11 panino",       0.50, 0.50),
        ("41b2fa7a-IMG_5963.jpeg", "12 anelletti",    0.50, 0.50),
        ("aff18a95-IMG_5815.jpeg", "13 pastries",     0.50, 0.50),
        ("48c8938b-IMG_5877.jpeg", "14 aperitivo",    0.50, 0.45),
        ("6fb5b683-IMG_5894.png",  "15 dog",          0.50, 0.55),
    ]),
    ("CH.4  TRAMONTO & ARRIVEDERCI", [
        ("1b426ca1-IMG_6084.jpeg", "16 chandelier",   0.50, 0.50),
        ("fc45aad8-IMG_5957.jpeg", "17 rooftop",      0.50, 0.45),
        ("19811080-IMG_5953.jpeg", "18 beer/duomo",   0.50, 0.50),
        ("692339f0-IMG_5960.jpeg", "19 sunset",       0.50, 0.50),
        ("10f28151-IMG_5788.jpeg", "20 plane home",   0.50, 0.50),
    ]),
]

TW, TH = 248, 441          # thumb 9:16
HDR = 34                   # chapter title bar
LBL = 22                   # per-thumb label strip
PAD = 12
COLS = 5

def crop916(im, hx, vy):
    im = ImageOps.exif_transpose(im).convert("RGB")
    w, h = im.size
    t = 9/16
    if w/h > t:
        nw = int(h*t); nh = h; x = int((w-nw)*hx); y = 0
    else:
        nw = w; nh = int(w/t); x = 0; y = int((h-nh)*vy)
    return im.crop((x, y, x+nw, y+nh)).resize((TW, TH), Image.LANCZOS)

cell_w = TW + PAD
row_h = HDR + LBL + TH + PAD
W = COLS*cell_w + PAD
H = len(CHAPTERS)*row_h + PAD + 44

canvas = Image.new("RGB", (W, H), (20, 20, 24))
d = ImageDraw.Draw(canvas)
ft = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
fc = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 19)
fl = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)

d.text((PAD, 14), "SICILY — 20 shots, 4 chapters of 5, 9:16  (post one chapter per drop)", font=ft, fill=(240,240,240))

for ci, (title, shots) in enumerate(CHAPTERS):
    oy = 44 + PAD + ci*row_h
    d.rectangle([PAD, oy, W-PAD, oy+HDR-4], fill=(46,46,54))
    d.text((PAD+10, oy+6), title, font=fc, fill=(255,210,120))
    for i, (fn, lbl, hx, vy) in enumerate(shots):
        ox = PAD + i*cell_w
        ty = oy + HDR
        d.text((ox+2, ty), lbl, font=fl, fill=(200,200,205))
        canvas.paste(crop916(Image.open(BASE+fn), hx, vy), (ox, ty+LBL))

OUT = "/home/user/website/sicily_chapters.jpg"
canvas.save(OUT, quality=90)
print("saved", OUT, canvas.size)
