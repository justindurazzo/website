import os
from PIL import Image

BASE = "/root/.claude/uploads/f650b114-7abe-53e3-98ba-153e056e5d84/"
OUT = "/home/user/website/story_export"
os.makedirs(OUT, exist_ok=True)

# same crop anchors as the approved v2 storyboard
SHOTS = [
    ("f640f635-suarfotos439.jpeg",          1, "the-room",        0.50, 0.15),
    ("95048462-suarfotos526.jpeg",          2, "you-hero",        0.50, 0.45),
    ("0bd1a363-suarfotos395.jpeg",          3, "the-dancer",      0.50, 0.35),
    ("a4680f28-suarfotos525.jpeg",          4, "you-crouch",      0.48, 0.45),
    ("3b2c58b3-suarfotos546_1.jpeg",        5, "david-vocals",    0.55, 0.45),
    ("84bc6df7-IMG_4387.png",               6, "you-confetti",    0.50, 0.50),
    ("770b324a-suarfotos523.jpeg",          7, "stage-edge",      0.55, 0.50),
    ("fa970d0b-Droga5_Reunion_6.9.26_pictureplastic__Mark_Minton128.jpeg", 8, "curtain-exit", 0.50, 0.45),
]

OW, OH = 1080, 1920
target = OW/OH

for fn, num, name, hx, vy in SHOTS:
    im = Image.open(BASE+fn).convert("RGB")
    w, h = im.size
    if w/h > target:                 # too wide -> crop width
        nw = int(h*target); nh = h
        x = int((w-nw)*hx); y = 0
    else:                            # too tall -> crop height
        nw = w; nh = int(w/target)
        x = 0; y = int((h-nh)*vy)
    crop = im.crop((x, y, x+nw, y+nh)).resize((OW, OH), Image.LANCZOS)
    out = f"{OUT}/story_{num}_{name}.jpg"
    crop.save(out, quality=95)
    print(out, crop.size)
