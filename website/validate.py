#!/usr/bin/env python3
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "website"
DIST = SITE / "dist"

required_source = ["index.html", "404.html", "site.css", "site.js", "_headers", "build.py"]
for name in required_source:
    if not (SITE / name).is_file():
        raise SystemExit(f"missing website source: {name}")

subprocess.run([sys.executable, str(SITE / "build.py")], cwd=ROOT, check=True)

required_dist = ["index.html", "404.html", "_headers", "assets/glaze.css", "assets/glaze.controls.css", "assets/glaze.accessibility.css", "assets/site.css", "assets/site.js"]
for name in required_dist:
    if not (DIST / name).is_file():
        raise SystemExit(f"missing build artifact: {name}")

html = (DIST / "index.html").read_text(encoding="utf-8")
headers = (DIST / "_headers").read_text(encoding="utf-8")
js = (DIST / "assets/site.js").read_text(encoding="utf-8")

for needle in ["Glaze UI 1.2.0", "Canvas", "Solid", "Raised", "Glaze", "Overlay", "Twelve gates", "Skip to content"]:
    if needle not in html:
        raise SystemExit(f"required public-site content missing: {needle}")

if "/assets/glaze.controls.css" not in html:
    raise SystemExit("Glaze UI 1.2 controls stylesheet is not loaded by the public site")

for remote in re.findall(r'(?:src|href)=["\'](https?://[^"\']+)', html):
    if "github.com/GoreeCloud/glaze-ui" not in remote:
        raise SystemExit(f"unexpected remote browser resource/link: {remote}")

for directive in ["Content-Security-Policy:", "frame-ancestors 'none'", "Permissions-Policy:", "X-Content-Type-Options: nosniff"]:
    if directive not in headers:
        raise SystemExit(f"required security header missing: {directive}")

if "localStorage" not in js or "data-theme-choice" not in html:
    raise SystemExit("local appearance preference contract missing")

print("Glaze UI public design site validation passed")
