"""Собирает версию для GitHub Pages в папку site/.

kuranty.html написан как фрагмент страницы (так его публикует claude.ai).
Здесь он оборачивается в полноценный документ, а рядом кладутся ассеты.
Запуск:  python build_site.py
"""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "kuranty.html"
OUT = ROOT / "site"
ASSETS = ["photo.jpg", "photo_clock.jpg", "side_bg.jpg", "sky_mask.png",
          "occl_R.png", "occl_L.png", "kuranty.mp4", "anthem.mp4"]

html = SRC.read_text(encoding="utf-8")
head_part, body_part = html.split("<canvas", 1)
body_part = "<canvas" + body_part
head_part = head_part.replace('<meta charset="utf-8">\n', "")

page = f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="theme-color" content="#07070c">
<meta name="description" content="Кремлёвские куранты: Спасская башня ночью, бой курантов по московскому времени, гимн и салют.">
{head_part.strip()}
</head>
<body>
{body_part.strip()}
</body>
</html>
"""

if OUT.exists():
    for p in OUT.iterdir():
        if p.name == ".git":
            continue
        shutil.rmtree(p) if p.is_dir() else p.unlink()
OUT.mkdir(exist_ok=True)
(OUT / "index.html").write_text(page, encoding="utf-8")
(OUT / ".nojekyll").write_text("", encoding="utf-8")
dst = OUT / "assets" / "web"
dst.mkdir(parents=True, exist_ok=True)
total = 0
for name in ASSETS:
    shutil.copy2(ROOT / "assets" / "web" / name, dst / name)
    total += (dst / name).stat().st_size
total += (OUT / "index.html").stat().st_size
print(f"site/ готов: index.html + {len(ASSETS)} файлов, {total / 1e6:.1f} МБ")
