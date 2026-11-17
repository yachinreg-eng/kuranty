from PIL import Image, ImageFilter, ImageEnhance
import numpy as np, pathlib
OUT = pathlib.Path(r"C:\Projects\NewYear\assets\web")
def soft_alpha(size, inner=0.56, outer=1.0):
    y, x = np.mgrid[0:size, 0:size]
    c = (size - 1) / 2
    d = np.sqrt((x - c) ** 2 + (y - c) ** 2) / (size / 2)
    a = 1.0 - np.clip((d - inner) / (outer - inner), 0, 1)
    a = a * a * (3 - 2 * a)
    return Image.fromarray((a * 255).astype("uint8"), "L").filter(ImageFilter.GaussianBlur(size * 0.014))
def night_grade(im):
    im = ImageEnhance.Color(im).enhance(1.04)
    im = ImageEnhance.Brightness(im).enhance(0.92)
    im = ImageEnhance.Contrast(im).enhance(1.10)
    return Image.blend(im, Image.new("RGB", im.size, (30, 40, 74)), 0.28)
def portrait(src, frac_center, frac_side, size=480):
    im = Image.open(src).convert("RGB"); W, H = im.size
    side = int(min(W, H) * frac_side)
    cx, cy = int(W * frac_center[0]), int(H * frac_center[1])
    x0 = max(0, min(W - side, cx - side // 2)); y0 = max(0, min(H - side, cy - side // 2))
    im = im.crop((x0, y0, x0 + side, y0 + side)).resize((size, size), Image.LANCZOS)
    out = night_grade(im).convert("RGBA"); out.putalpha(soft_alpha(size)); return out
portrait(r"_img\E.jpg", (0.50, 0.40), 0.78).save(OUT/"greet_dm.png", optimize=True)
portrait(r"_img\D.jpg", (0.53, 0.33), 0.54).save(OUT/"greet_sneg.png", optimize=True)
print("ok")
