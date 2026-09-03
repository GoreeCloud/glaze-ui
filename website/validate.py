#!/usr/bin/env python3
from pathlib import Path
import hashlib
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "website"
DIST = SITE / "dist"
IDENTITY = ROOT / "assets" / "identity" / "official" / "facet"
CANONICAL_SHA256 = "3c9566bf21c5bed4121547c3d5c79c34e4f3e60105179b7f2342c4b60ae91a61"

for name in ("index.html", "404.html", "site.css", "identity.css", "site.js", "_headers", "build.py"):
    if not (SITE / name).is_file():
        raise SystemExit(f"missing website source: {name}")

for forbidden in (
    ROOT / "assets" / "identity" / "candidates" / "round-4",
    ROOT / "assets" / "identity" / "official" / "fold",
):
    if forbidden.exists():
        raise SystemExit(
            f"non-canonical identity path must not exist: {forbidden.relative_to(ROOT)}"
        )

mark = IDENTITY / "glaze-ui-mark.svg"
if not mark.is_file() or hashlib.sha256(mark.read_bytes()).hexdigest() != CANONICAL_SHA256:
    raise SystemExit("synchronized Facet source missing or changed")

subprocess.run([sys.executable, str(SITE / "build.py")], cwd=ROOT, check=True)

required = (
    "index.html",
    "404.html",
    "_headers",
    "reference/v1-system-shell.html",
    "assets/site.css",
    "assets/identity.css",
    "assets/site.js",
    "assets/glaze-ui-mark.svg",
    "assets/glaze.css",
    "assets/glaze.controls.css",
    "assets/glaze.expressive.css",
    "assets/glaze.formfactors.css",
    "assets/glaze.accessibility.css",
    "assets/glaze.color.css",
    "assets/glaze.motion.css",
    "assets/glaze.materials.css",
    "assets/glaze.layout.css",
    "assets/glaze.states.css",
    "assets/glaze-v1.0.0.css",
    "assets/glaze-v1.foundation.css",
    "assets/glaze-v1.components.css",
    "assets/glaze-v1.components.adaptive.css",
    "assets/glaze-v1.components.runtime.css",
    "assets/glaze-v1.structure.css",
    "assets/glaze-v1.overlay.css",
    "assets/glaze-v1.advanced.css",
    "assets/glaze-v1.visual-refinement.css",
    "assets/glaze-v1.optical-reachability.css",
)
for name in required:
    if not (DIST / name).is_file():
        raise SystemExit(f"missing build artifact: {name}")

if (DIST / "assets" / "glaze-ui-mark.svg").read_bytes() != mark.read_bytes():
    raise SystemExit("public identity asset drifted from Facet source")

# The public artifact may contain generic shared foundations and V1 assets only.
# Former product-release/candidate namespaces are not valid current publication
# inputs, even when Git history retains them for audit and rollback purposes.
legacy_filename_markers = (
    "glaze-2.",
    "glaze-2-",
    "glaze-2_",
    "candidate",
    "2.2.0",
    "2.1.0",
    "2.0.0",
)
for path in DIST.rglob("*"):
    if path.is_file():
        rel = path.relative_to(DIST).as_posix().lower()
        if any(marker in rel for marker in legacy_filename_markers):
            raise SystemExit(f"former release namespace published in V1 artifact: {rel}")

html = (DIST / "index.html").read_text(encoding="utf-8")
not_found = (DIST / "404.html").read_text(encoding="utf-8")
headers = (DIST / "_headers").read_text(encoding="utf-8")
js = (DIST / "assets" / "site.js").read_text(encoding="utf-8")
entrypoint = (DIST / "assets" / "glaze-v1.0.0.css").read_text(encoding="utf-8")

for text in (
    "GLAZE UI V1.0",
    "Machine version <strong>1.0.0</strong>",
    "Solid where you read. Glazed where you interact.",
    "Workspace → Application → System Overlay → System Panel → Critical System",
    "one dominant Glaze panel plus one to three small floating Glaze controls",
    "32 bounded contracts across five tiers.",
    "Universal Search",
    "Control Center",
    "Production revalidation",
    "exact source revision",
    "GoreeCloud/goreecloud-glaze-ui",
    "Skip to content",
):
    if text not in html:
        raise SystemExit(f"required V1 Design Center content missing: {text}")

for text in (
    "Glaze UI 2.2",
    "GLAZE UI 2.2",
    "2.2 is Stable",
    "2.1.0",
    "2.0.0",
    "glaze-2.",
    "glaze-v1.0.css",
    "glz22",
):
    if text.lower() in html.lower() or text.lower() in not_found.lower():
        raise SystemExit(f"former release content leaked into V1 public surface: {text}")

for text in (
    "GLAZE UI V1.0",
    "404 · GLAZE UI V1.0",
    "/assets/glaze-v1.0.0.css",
):
    if text not in not_found:
        raise SystemExit(f"V1 404 surface missing: {text}")

for marker in (
    '@import url("./glaze-v1.foundation.css")',
    '@import url("./glaze-v1.components.css")',
    '@import url("./glaze-v1.components.adaptive.css")',
    '@import url("./glaze-v1.components.runtime.css")',
    '@import url("./glaze-v1.structure.css")',
    '@import url("./glaze-v1.overlay.css")',
    '@import url("./glaze-v1.advanced.css")',
    '@import url("./glaze-v1.visual-refinement.css")',
    '@import url("./glaze-v1.optical-reachability.css")',
):
    if marker not in entrypoint:
        raise SystemExit(f"V1 entrypoint missing required source layer: {marker}")

# Every local published asset referenced by the two HTML entry surfaces must exist.
for surface_name, surface in (("index", html), ("404", not_found)):
    for asset in re.findall(r'(?:src|href)=["\'](/assets/[^"\']+)', surface):
        if not (DIST / asset.removeprefix("/")).is_file():
            raise SystemExit(f"{surface_name} references missing public asset: {asset}")

if "/reference/v1-system-shell.html" not in html:
    raise SystemExit("V1 System Shell public reference link missing")

for remote in re.findall(r'(?:src|href)=["\'](https?://[^"\']+)', html + not_found):
    if "github.com/GoreeCloud/goreecloud-glaze-ui" not in remote:
        raise SystemExit(f"unexpected remote browser resource/link: {remote}")

for directive in (
    "Content-Security-Policy:",
    "frame-ancestors 'none'",
    "Permissions-Policy:",
    "X-Content-Type-Options: nosniff",
):
    if directive not in headers:
        raise SystemExit(f"required security header missing: {directive}")

if "localStorage" not in js or "data-theme-choice" not in html:
    raise SystemExit("local appearance preference contract missing")

print(
    "GLAZE UI V1.0 Design Center validation passed: isolated V1 publication, "
    "synchronized Facet identity, required security headers, and exact-reset "
    "production-revalidation disclosure"
)
