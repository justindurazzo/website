from PIL import Image, ImageOps

src = "/root/.claude/uploads/f650b114-7abe-53e3-98ba-153e056e5d84/f07c6889-IMG_6090.jpeg"
photo = ImageOps.exif_transpose(Image.open(src)).convert("RGB")

# canvas = aspect ratio / size of the uploaded screenshot (the IG story canvas)
CW, CH = 1206, 2622
SIDE = 60                      # side border; photo kept UNCROPPED and centered

pw_full, ph_full = photo.size
target_w = CW - 2*SIDE
target_h = int(target_w * ph_full / pw_full)   # keep photo's own aspect (no crop)
if target_h > CH - 2*SIDE:                      # safety: don't exceed canvas height
    target_h = CH - 2*SIDE
    target_w = int(target_h * pw_full / ph_full)
ph = photo.resize((target_w, target_h), Image.LANCZOS)

canvas = Image.new("RGB", (CW, CH), (255, 255, 255))
x = (CW - target_w)//2
y = (CH - target_h)//2
canvas.paste(ph, (x, y))
out = "/home/user/website/sicily_export/madonna_framed.jpg"
canvas.save(out, quality=95)
print("canvas", canvas.size, "photo", ph.size, "margins L/R", x, "T/B", y)
