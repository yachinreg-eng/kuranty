"""Готовит портреты для открытки: два круга с мягкими краями из одного фото.

Источник: Wikimedia Commons, File:Dedmoroz2.jpg (Дед Мороз и Снегурочка в
деревянной горнице), CC BY-SA 4.0. Скрипт скачивает фото, вырезает два
квадрата (Дед Мороз и Снегурочка), тонирует их под ночную сцену и гасит
края радиальной маской, чтобы портреты растворялись в тёмном фоне.

    python make_portraits.py            # положит greet_dm.png и greet_sneg.png в assets/web
"""

import pathlib
import subprocess
import sys

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

WEB = pathlib.Path(__file__).resolve().parents[1] / "web"
CACHE = pathlib.Path(__file__).resolve().parent / "_cache"
SOURCE_URL = (
    "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/Dedmoroz2.jpg/"
    "1920px-Dedmoroz2.jpg"
)
SIZE = 480

# центр кропа в долях кадра и сторона квадрата в долях меньшей стороны
CROPS = {
    "greet_dm.png": (0.657, 0.320, 0.26),    # Дед Мороз в красной шубе с посохом
    "greet_sneg.png": (0.288, 0.275, 0.26),  # Снегурочка в кокошнике
}


def soft_alpha(size, inner=0.56, outer=1.0):
    """Радиальная маска: 1 в центре, плавный спад к краю, лёгкое размытие."""
    y, x = np.mgrid[0:size, 0:size]
    c = (size - 1) / 2
    d = np.sqrt((x - c) ** 2 + (y - c) ** 2) / (size / 2)
    a = 1.0 - np.clip((d - inner) / (outer - inner), 0, 1)
    a = a * a * (3 - 2 * a)
    return Image.fromarray((a * 255).astype("uint8"), "L").filter(
        ImageFilter.GaussianBlur(size * 0.014)
    )


def night_grade(im, bright=0.95, tint=0.24):
    """Приглушает яркость и подмешивает холодный синий — под ночное небо."""
    im = ImageEnhance.Color(im).enhance(1.05)
    im = ImageEnhance.Brightness(im).enhance(bright)
    im = ImageEnhance.Contrast(im).enhance(1.10)
    return Image.blend(im, Image.new("RGB", im.size, (34, 44, 78)), tint)


def portrait(src, cx_f, cy_f, side_f, size=SIZE):
    im = Image.open(src).convert("RGB")
    w, h = im.size
    side = int(min(w, h) * side_f)
    cx, cy = int(w * cx_f), int(h * cy_f)
    x0 = max(0, min(w - side, cx - side // 2))
    y0 = max(0, min(h - side, cy - side // 2))
    im = im.crop((x0, y0, x0 + side, y0 + side)).resize((size, size), Image.LANCZOS)
    out = night_grade(im).convert("RGBA")
    out.putalpha(soft_alpha(size))
    return out


def main():
    CACHE.mkdir(exist_ok=True)
    src = CACHE / "dedmoroz2.jpg"
    if not src.exists():
        # без Referer Wikimedia отдаёт пустой ответ
        subprocess.run(
            [
                "curl.exe", "-s", "-L", "-A", "dsh-agent/1.0",
                "-H", "Referer: https://commons.wikimedia.org/",
                "-o", str(src), SOURCE_URL,
            ],
            check=True,
        )
    for name, (cx, cy, side) in CROPS.items():
        portrait(src, cx, cy, side).save(WEB / name, optimize=True)
        print(name, (WEB / name).stat().st_size, "bytes")


if __name__ == "__main__":
    sys.exit(main())
