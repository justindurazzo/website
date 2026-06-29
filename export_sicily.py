import os
from PIL import Image, ImageOps

BASE = "/root/.claude/uploads/f650b114-7abe-53e3-98ba-153e056e5d84/"
OUT = "/home/user/website/sicily_export"
os.makedirs(OUT, exist_ok=True)

# (file, global#, chapter, slot-in-chapter, name, hx, vy)
SHOTS = [
    ("ba697cea-IMG_5836.jpeg", 1, 1, 1, "tabacchi",    0.50, 0.50),
    ("e0980238-IMG_6142.jpeg", 2, 1, 2, "balcony-man", 0.50, 0.50),
    ("36b629d6-IMG_6065.jpeg", 3, 1, 3, "horse",       0.50, 0.45),
    ("f5ffbb44-IMG_5860.jpeg", 4, 1, 4, "antiques",    0.50, 0.45),
    ("361ce422-IMG_6118.jpeg", 5, 1, 5, "souvenirs",   0.50, 0.50),

    ("4c780564-IMG_6026.jpeg", 6, 2, 1, "seafood",     0.50, 0.50),
    ("f4a22a6d-IMG_6034.jpeg", 7, 2, 2, "olives",      0.50, 0.45),
    ("d454f098-IMG_6121.jpeg", 8, 2, 3, "lemon-shirt", 0.50, 0.50),
    ("f07c6889-IMG_6090.jpeg", 9, 2, 4, "madonna",     0.50, 0.50),
    ("ca74efdf-IMG_6047.jpeg",10, 2, 5, "porchetta",   0.50, 0.45),
    ("253e6871-IMG_5871.jpeg",11, 2, 6, "you-mirror",  0.50, 0.50),

    ("8fffc94a-IMG_6070.jpeg",12, 3, 1, "panino",      0.50, 0.50),
    ("41b2fa7a-IMG_5963.jpeg",13, 3, 2, "anelletti",   0.50, 0.50),
    ("aff18a95-IMG_5815.jpeg",14, 3, 3, "pastries",    0.50, 0.50),
    ("48c8938b-IMG_5877.jpeg",15, 3, 4, "aperitivo",   0.50, 0.45),
    ("6fb5b683-IMG_5894.png", 16, 3, 5, "dog",         0.50, 0.55),

    ("1b426ca1-IMG_6084.jpeg",17, 4, 1, "chandelier",  0.50, 0.50),
    ("fc45aad8-IMG_5957.jpeg",18, 4, 2, "rooftop",     0.50, 0.45),
    ("19811080-IMG_5953.jpeg",19, 4, 3, "beer-duomo",  0.50, 0.50),
    ("692339f0-IMG_5960.jpeg",20, 4, 4, "sunset",      0.50, 0.50),
    ("10f28151-IMG_5788.jpeg",21, 4, 5, "plane-home",  0.50, 0.50),
]

OW, OH = 1080, 1920
t = OW/OH

for fn, g, ch, slot, name, hx, vy in SHOTS:
    im = ImageOps.exif_transpose(Image.open(BASE+fn)).convert("RGB")
    w, h = im.size
    if w/h > t:
        nw = int(h*t); nh = h; x = int((w-nw)*hx); y = 0
    else:
        nw = w; nh = int(w/t); x = 0; y = int((h-nh)*vy)
    crop = im.crop((x, y, x+nw, y+nh)).resize((OW, OH), Image.LANCZOS)
    out = f"{OUT}/ch{ch}_{slot}_{g:02d}_{name}.jpg"
    crop.save(out, quality=95)
    print(out)
