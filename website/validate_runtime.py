#!/usr/bin/env python3
"""Validate the public Design Center's actual GLAZE UI V1.1 runtime activation."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "website"
DIST = SITE / "dist"

index = (SITE / "index.html").read_text(encoding="utf-8")
not_found = (SITE / "404.html").read_text(encoding="utf-8")
js = (SITE / "site.js").read_text(encoding="utf-8")
runtime_css = (SITE / "runtime-fixes.css").read_text(encoding="utf-8")
built_css = (DIST / "assets" / "site.css").read_text(encoding="utf-8")

for name, document in (("index", index), ("404", not_found)):
    if 'data-glaze-version="1.1"' not in document:
        raise SystemExit(f"{name} does not activate GLAZE UI V1.1")
    if 'name="goreecloud-glaze-ui" content="1.1.0"' not in document:
        raise SystemExit(f"{name} lacks the 1.1.0 public version marker")
    if 'data-glaze-ui="1.1.0"' not in document:
        raise SystemExit(f"{name} lacks the 1.1.0 stylesheet marker")
    if re.search(r'\sstyle=["\']', document, re.IGNORECASE):
        raise SystemExit(f"{name} contains inline style blocked by the public CSP")

for marker in ("glz11-atmosphere", "glz11-nav", "glz11-nav-item", "glz11-button", "deep-dark"):
    if marker not in index:
        raise SystemExit(f"Design Center V1.1 runtime marker missing: {marker}")

if "data-glz-appearance" not in js:
    raise SystemExit("Design Center script does not use the V1.1 data-glz-appearance contract")
if "data-glaze-appearance" in js:
    raise SystemExit("obsolete data-glaze-appearance contract remains active")
for mode in ("system", "light", "dark", "deep-dark"):
    if mode not in js:
        raise SystemExit(f"Design Center appearance mode missing: {mode}")

for marker in ("prefers-reduced-transparency:reduce", "prefers-contrast:more", "@media print"):
    if marker not in runtime_css:
        raise SystemExit(f"Design Center runtime fallback missing: {marker}")
if runtime_css not in built_css:
    raise SystemExit("CSP-safe runtime fixes were not included in the built product stylesheet")

print("Design Center V1.1 runtime validation passed: declarative activation, current appearance contract, CSP-safe styling, Deep Dark support, and accessibility fallbacks are present.")
