# Кремлёвские куранты — исходники

Публикуемый сайт живёт в ветке `main` (её и отдаёт GitHub Pages: https://yachinreg-eng.github.io/kuranty/).
Эта ветка, `source`, — рабочая: из неё собирается `main`.

## Сборка

```powershell
python build_site.py
```

`build_site.py` берёт `kuranty.html` (фрагмент страницы без `<html>`, как его отдаёт claude.ai),
дописывает шапку с `lang="ru"`, кладёт готовый `site/index.html`, `site/.nojekyll`
и копирует 8 файлов из `assets/web` в `site/assets/web`.

Затем содержимое `site/` уходит в ветку `main` (например, `git subtree` или просто копированием).

## Что где

- `kuranty.html` — вся сцена: canvas, циферблаты поверх фото, снег, салют, куранты, гимн, радио.
- `build_site.py` — сборщик страницы и ассетов.
- `ДЕПЛОЙ.md` — как публиковать.
- `assets/web/` — облегчённые ассеты, которые уезжают на сайт (фото, видео боя и гимна, маски).
- `assets/src/` — исходники: `spasskaya_2015.jpg` (13 МБ) и запись боя `address_2011_240p.webm` (9 МБ).
- `.claude/launch.json` — локальный сервер `python -m http.server 8765`.
