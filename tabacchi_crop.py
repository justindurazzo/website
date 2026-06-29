from PIL import Image, ImageOps

src = "/root/.claude/uploads/f650b114-7abe-53e3-98ba-153e056e5d84/ba697cea-IMG_5836.jpeg"
im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
w, h = im.size  # 2268 x 4032 (already ~9:16)
print("orig", im.size)

# tighter 9:16 crop: zoom in, push the sign right-of-center (window anchored left), nudge up
ZOOM = 1.18
HX, VY = 0.36, 0.42     # window center bias: <0.5 = keep more LEFT -> sign sits right
t = 9/16

nw = int(w/ZOOM)
nh = int(nw/t)
if nh > h:
    nh = h; nw = int(nh*t)
x = int((w-nw)*HX)
y = int((h-nh)*VY)
crop = im.crop((x, y, x+nw, y+nh)).resize((1080,1920), Image.LANCZOS)
crop.save("/home/user/website/sicily_export/ch1_1_01_tabacchi.jpg", quality=95)
print("saved", crop.size)
