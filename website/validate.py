#!/usr/bin/env python3
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "website"
DIST = SITE / "dist"

required_source = ["index.html", "404.html", "site.css", "site.js", "glaze-ui-mark.svg", "_headers", "build.py"]
for name in required_source:
    if not (SITE / name).is_file():
        raise SystemExit(f"missing website source: {name}")

subprocess.run([sys.executable, str(SITE / "build.py")], cwd=ROOT, check=True)

required_dist = [
    "index.html",
    "404.html",
    "_headers",
    "assets/glaze.css",
    "assets/glaze.controls.css",
    "assets/glaze.expressive.css",
    "assets/glaze.accessibility.css",
    "assets/site.css",
    "assets/site.js",
    "assets/glaze-ui-mark.svg",
]
for name in required_dist:
    if not (DIST / name).is_file():
        raise SystemExit(f"missing build artifact: {name}")

html = (DIST / "index.html").read_text(encoding="utf-8")
headers = (DIST / "_headers").read_text(encoding="utf-8")
js = (DIST / "assets/site.js").read_text(encoding="utf-8")
expressive = (DIST / "assets/glaze.expressive.css").read_text(encoding="utf-8")
mark = (DIST / "assets/glaze-ui-mark.svg").read_text(encoding="utf-8")

for needle in [
    "Glaze UI 1.3.0",
    "Stable",
    "Calm structure.",
    "Expressive moments.",
    "Canvas",
    "Solid",
    "Raised",
    "Glaze",
    "Overlay",
    "Functional Glass",
    "Fifteen gates",
    "Skip to content",
    "/assets/glaze-ui-mark.svg",
    "Privacy by default",
]:
    if needle not in html:
        raise SystemExit(f"required public-site content missing: {needle}")

if "Glaze UI mark" not in mark or "linearGradient" not in mark:
    raise SystemExit("Glaze UI identity artwork contract missing")

for stylesheet in ("/assets/glaze.controls.css", "/assets/glaze.expressive.css", "/assets/glaze.accessibility.css"):
    if stylesheet not in html:
        raise SystemExit(f"Glaze UI required stylesheet is not loaded by the public site: {stylesheet}")

for marker in (
    ".glaze-glass-functional",
    ".glaze-glass-clear",
    ".glaze-expressive-action",
    ".glaze-button-group",
    ".glaze-reach-layout",
    "prefers-reduced-motion",
    "prefers-reduced-transparency",
    "forced-colors",
):
    if marker not in expressive:
        raise SystemExit(f"expressive layer contract missing: {marker}")

allowed_link_hosts = {"www.goreecloud.com", "projects.goreecloud.com", "github.com"}
for remote in re.findall(r'(?:src|href)=["\'](https?://[^"\']+)', html):
    parsed = urlparse(remote)
    if parsed.hostname not in allowed_link_hosts:
        raise SystemExit(f"unexpected remote public link: {remote}")
    if parsed.hostname == "github.com" and not parsed.path.startswith("/GoreeCloud/glaze-ui"):
        raise SystemExit(f"unexpected GitHub destination: {remote}")

# Cross-site destinations may be links, but browser resources must remain local.
for attribute, remote in re.findall(r'(src|href)=["\'](https?://[^"\']+)', html):
    if attribute == "src":
        raise SystemExit(f"remote browser resource is prohibited: {remote}")

for directive in ["Content-Security-Policy:", "frame-ancestors 'none'", "Permissions-Policy:", "X-Content-Type-Options: nosniff"]:
    if directive not in headers:
        raise SystemExit(f"required security header missing: {directive}")

if "localStorage" not in js or "data-theme-choice" not in html:
    raise SystemExit("local appearance preference contract missing")

print("Glaze UI 1.3 Stable public design site validation passed")
