"""Reconstruit index.html à partir des sources du dossier src/.

Utilisation :  python3 build.py
"""
import base64
from pathlib import Path

SRC = Path(__file__).parent / "src"


def data_uri(nom, mime):
    return f"data:{mime};base64," + base64.b64encode((SRC / nom).read_bytes()).decode()


html = (SRC / "site.html").read_text(encoding="utf-8")
html = (html
        .replace("__CSS__", (SRC / "base.css").read_text(encoding="utf-8"))
        .replace("__LOGOPNG__", data_uri("logo.webp", "image/webp"))
        .replace("__LOGO__", data_uri("logo.jpg", "image/jpeg"))
        .replace("__DATA__", (SRC / "produits.txt").read_text(encoding="utf-8"))
        .replace("__PHOTOS__", (SRC / "photos.csv").read_text(encoding="utf-8").strip()))
(Path(__file__).parent / "index.html").write_text(html, encoding="utf-8")
print("index.html reconstruit")
