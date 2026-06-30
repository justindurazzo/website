from PIL import Image, ImageOps

src = "/root/.claude/uploads/f650b114-7abe-53e3-98ba-153e056e5d84/f07c6889-IMG_6090.jpeg"
im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")

OW, OH = 1080, 1920
B = 54                      # even border, all four sides
iw, ih = OW - 2*B, OH - 2*B
inner_t = iw/ih

w, h = im.size
if w/h > inner_t:           # crop width to match inner box aspect
    nw = int(h*inner_t); nh = h
else:                       # crop height
    nw = w; nh = int(w/inner_t)
x = (w-nw)//2; y = (h-nh)//2
photo = im.crop((x, y, x+nw, y+nh)).resize((iw, ih), Image.LANCZOS)

canvas = Image.new("RGB", (OW, OH), (255, 255, 255))
canvas.paste(photo, (B, B))
out = "/home/user/website/sicily_export/madonna_framed.jpg"
canvas.save(out, quality=95)
print("saved", out, "border", B, "px all sides")
