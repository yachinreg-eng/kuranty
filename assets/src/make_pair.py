"""Готовит фотографию для открытки: два героя рядом, края растворены.

Источник — pair_source.png (фото Деда Мороза и Снегурочки, предоставлено
автором сайта). Скрипт вырезает кадр с лицами, чуть притемняет его под ночную
сцену и гасит края, чтобы прямоугольник не «врезался» в открытку.

    python make_pair.py     # положит assets/web/greet_pair.png
"""

import pathlib
import sys

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

WEB = pathlib.Path(__file__).resolve().parents[1] / "web"
SRC = pathlib.Path(__file__).resolve().parent / "pair_source.png"

# кадр с двумя лицами (в пикселях исходника 1024x1536) и размер готовой картинки
CROP = (0, 210, 1024, 1030)
SIZE = (720, 576)
CORNER = 36
FEATHER = 16


def main():
    if not SRC.exists():
        raise SystemExit(f"нет исходника: {SRC}")

    im = Image.open(SRC).convert("RGB").crop(CROP).resize(SIZE, Image.LANCZOS)
    im = ImageEnhance.Brightness(im).enhance(0.96)
    im = ImageEnhance.Contrast(im).enhance(1.05)
    # холодный тон, чтобы фотография жила в ночной открытке
    im = Image.blend(im, Image.new("RGB", im.size, (26, 34, 62)), 0.12)

    w, h = im.size
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        (14, 14, w - 14, h - 14), radius=CORNER, fill=255
    )
    mask = mask.filter(ImageFilter.GaussianBlur(FEATHER))

    out = im.convert("RGBA")
    out.putalpha(mask)
    dst = WEB / "greet_pair.png"
    out.save(dst, optimize=True)
    print("greet_pair.png", dst.stat().st_size, "bytes", out.size)


if __name__ == "__main__":
    sys.exit(main())
