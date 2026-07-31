"""
build.py — Static site generator sederhana.

Cara pakai:
    python3 build.py

Yang terjadi:
1. Baca semua konten dari data/content.json
2. Render templates/index.html.j2 jadi HTML jadi
3. Simpan hasilnya (+ style.css + folder images) ke docs/
   -> folder docs/ inilah yang di-deploy ke GitHub Pages

Kalau mau ubah teks, harga, foto, dll -> cukup edit data/content.json
dan foto-foto di static/images/, lalu jalankan ulang script ini.
Tidak perlu sentuh file .html atau .css sama sekali.
"""

import json
import shutil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).parent
DATA_FILE = ROOT / "data" / "content.json"
TEMPLATES_DIR = ROOT / "templates"
STATIC_DIR = ROOT / "static"
OUTPUT_DIR = ROOT / "docs"


def load_content() -> dict:
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def render_html(content: dict) -> str:
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape(["html"]),
    )
    template = env.get_template("index.html.j2")
    return template.render(**content)


def copy_static_assets():
    shutil.copy(STATIC_DIR / "style.css", OUTPUT_DIR / "style.css")

    src_images = STATIC_DIR / "images"
    dst_images = OUTPUT_DIR / "images"
    if dst_images.exists():
        shutil.rmtree(dst_images)
    if src_images.exists():
        shutil.copytree(src_images, dst_images)
    else:
        dst_images.mkdir(parents=True, exist_ok=True)


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    content = load_content()
    html = render_html(content)

    (OUTPUT_DIR / "index.html").write_text(html, encoding="utf-8")
    copy_static_assets()

    (OUTPUT_DIR / ".nojekyll").touch()

    print("Selesai! Website statis ada di folder docs/")


if __name__ == "__main__":
    main()
