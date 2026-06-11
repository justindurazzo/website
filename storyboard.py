from PIL import Image, ImageDraw, ImageFont

BASE = "/root/.claude/uploads/f650b114-7abe-53e3-98ba-153e056e5d84/"

# (file, slot#, label, h_anchor 0..1, v_anchor 0..1)
# anchors: where the crop window is biased. 0.5 = center.
SHOTS = [
    ("f640f635-suarfotos439.jpeg",          1, "THE ROOM",        0.50, 0.15),
    ("b363ef58-suarfotos511.jpeg",          2, "BAND (WIDE)",     0.50, 0.45),
    ("0bd1a363-suarfotos395.jpeg",          3, "THE DANCER",      0.50, 0.35),
    ("95048462-suarfotos526.jpeg",          4, "YOU - HERO",      0.50, 0.45),
    ("3b2c58b3-suarfotos546_1.jpeg",        5, "DAVID (VOCALS)",  0.55, 0.45),
    ("a4680f28-suarfotos525.jpeg",          6, "YOU - CROUCH",    0.48, 0.45),
    ("f058fd3c-IMG_4384.jpeg",              7, "STAGE EDGE",      0.50, 0.50),  # USER's own crop of 523
    ("ac380085-suarfotos522.jpeg",          8, "BAND (DRINK)",    0.50, 0.45),
    ("84bc6df7-IMG_4387.png",               9, "YOU - CONFETTI",  0.50, 0.50),
    ("fa970d0b-Droga5_Reunion_6.9.26_pictureplastic__Mark_Minton128.jpeg", 10, "CURTAIN / EXIT", 0.50, 0.45),
]

TW, TH = 360, 640          # thumb 9:16
HDR = 54                   # header strip per thumb
PAD = 18
COLS = 5
ROWS = 2

def crop_916(im, hx, vy):
    w, h = im.size
    target = 9/16
    if w/h > target:                 # too wide -> crop width
        nw = int(h*target); nh = h
        x = int((w-nw)*hx); y = 0
    else:                            # too tall/narrow -> crop height
        nw = w; nh = int(w/target)
        x = 0; y = int((h-nh)*vy)
    return im.crop((x, y, x+nw, y+nh)).resize((TW, TH), Image.LANCZOS)

cell_w = TW + PAD
cell_h = TH + HDR + PAD
W = COLS*cell_w + PAD
H = ROWS*cell_h + PAD + 60   # +title bar

canvas = Image.new("RGB", (W, H), (18, 18, 20))
d = ImageDraw.Draw(canvas)

fbig  = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
fnum  = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
flbl  = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 19)

d.text((PAD, 18), "IG STORY SET v8 — 10 slots, 9:16  (#7 = your own stage-edge crop)",
       font=flbl, fill=(235,235,235))

for i, (fn, num, lbl, hx, vy) in enumerate(SHOTS):
    r, c = divmod(i, COLS)
    ox = PAD + c*cell_w
    oy = 60 + PAD + r*cell_h
    # header
    d.rectangle([ox, oy, ox+TW, oy+HDR], fill=(38,38,44))
    d.text((ox+12, oy+10), str(num), font=fnum, fill=(255,210,80))
    d.text((ox+48, oy+9),  lbl,  font=flbl, fill=(240,240,240))
    # image
    im = Image.open(BASE+fn).convert("RGB")
    canvas.paste(crop_916(im, hx, vy), (ox, oy+HDR))

OUT = "/home/user/website/ig_story_set.jpg"
canvas.save(OUT, quality=90)
print("saved", OUT, canvas.size)
