"""Construit le site publiable dans le dossier public/ à partir des sources de src/.

Utilisation :  python3 build.py

Produit :
  public/index.html               le site (HTML + CSS + JS + catalogue + logo)
  public/_headers                 en-têtes de sécurité HTTP lus par Netlify (CSP, HSTS…)
  public/.well-known/security.txt contact pour signaler une vulnérabilité (RFC 9116)
  public/fonts/, public/vendor/   polices et bibliothèques hébergées sur le site
"""
import base64
import hashlib
import re
import shutil
from datetime import datetime, timedelta, timezone
from pathlib import Path

RACINE = Path(__file__).parent
SRC = RACINE / "src"
PUBLIC = RACINE / "public"
SITE = "https://allinevent.netlify.app"
CONTACT_SECURITE = "mailto:quentinlo@icloud.com"


def data_uri(nom, mime):
    return f"data:{mime};base64," + base64.b64encode((SRC / nom).read_bytes()).decode()


# 1. Assemble index.html -------------------------------------------------------
html = (SRC / "site.html").read_text(encoding="utf-8")
html = (html
        .replace("__CSS__", (SRC / "base.css").read_text(encoding="utf-8"))
        .replace("__LOGOPNG__", data_uri("logo.webp", "image/webp"))
        .replace("__LOGO__", data_uri("logo.jpg", "image/jpeg"))
        .replace("__DATA__", (SRC / "produits.txt").read_text(encoding="utf-8"))
        .replace("__PHOTOS__", (SRC / "photos.csv").read_text(encoding="utf-8").strip()))

if PUBLIC.exists():
    shutil.rmtree(PUBLIC)
PUBLIC.mkdir()
(PUBLIC / "index.html").write_text(html, encoding="utf-8")

# 2. Polices et bibliothèques hébergées localement ----------------------------------
shutil.copytree(SRC / "fonts", PUBLIC / "fonts")
shutil.copytree(SRC / "vendor", PUBLIC / "vendor")

# 3. Empreintes des scripts inline pour la CSP (pas de 'unsafe-inline' pour les scripts)
scripts_inline = re.findall(r"<script>(.*?)</script>", html, flags=re.S)
empreintes = " ".join(
    "'sha256-" + base64.b64encode(hashlib.sha256(s.encode("utf-8")).digest()).decode() + "'"
    for s in scripts_inline
)

csp = "; ".join([
    "default-src 'self'",
    f"script-src 'self' {empreintes}",
    "style-src 'self' 'unsafe-inline'",
    "img-src 'self' data: blob: https://images.unsplash.com",
    "media-src 'self' https://videos.pexels.com",
    "font-src 'self'",
    "connect-src 'self'",
    "form-action 'self'",
    "frame-ancestors 'none'",
    "base-uri 'self'",
    "object-src 'none'",
    "upgrade-insecure-requests",
])

(PUBLIC / "_headers").write_text(f"""/*
  Content-Security-Policy: {csp}
  Strict-Transport-Security: max-age=31536000; includeSubDomains
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=(), magnetometer=(), gyroscope=(), accelerometer=()
  Cross-Origin-Opener-Policy: same-origin
  X-Permitted-Cross-Domain-Policies: none

/fonts/*
  Cache-Control: public, max-age=31536000, immutable

/vendor/*
  Cache-Control: public, max-age=31536000, immutable

/.well-known/security.txt
  Content-Type: text/plain; charset=utf-8
""", encoding="utf-8")

# 4. security.txt (RFC 9116), valable un an ----------------------------------------
expire = (datetime.now(timezone.utc) + timedelta(days=365)).strftime("%Y-%m-%dT00:00:00.000Z")
(PUBLIC / ".well-known").mkdir()
(PUBLIC / ".well-known" / "security.txt").write_text(f"""# Signaler une vulnérabilité sur le site All In Évent
Contact: {CONTACT_SECURITE}
Expires: {expire}
Preferred-Languages: fr, en
Canonical: {SITE}/.well-known/security.txt
Policy: {SITE}/#mentions
""", encoding="utf-8")

print(f"public/ construit ({len(scripts_inline)} script(s) inline protégé(s) par empreinte CSP)")
