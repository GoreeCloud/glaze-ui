#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOKENS = ROOT / "tokens" / "layout.json"
DOC = ROOT / "LAYOUT.md"
CSS = ROOT / "css" / "glaze.layout.css"


def fail(message: str) -> None:
    raise SystemExit(f"layout validation failed: {message}")


for path in (TOKENS, DOC, CSS):
    if not path.is_file():
        fail(f"missing {path.relative_to(ROOT)}")

try:
    data = json.loads(TOKENS.read_text())
except Exception as exc:
    fail(f"invalid JSON: {exc}")

if data.get("status") != "1.5-stable":
    fail("token status must remain 1.5-stable")
if data.get("stableBaseline") != "1.5.0":
    fail("stable baseline must remain 1.5.0")

expected_space = ["2", "4", "8", "12", "16", "24", "32", "48", "64", "96"]
if list(data.get("space", {}).keys()) != expected_space:
    fail("canonical spacing scale changed")

for role in ("hairline", "controlGap", "clusterGap", "contentGap", "sectionGap", "regionGap", "pageGap"):
    if role not in data.get("semanticSpacing", {}):
        fail(f"missing semantic spacing role {role}")

if data.get("gutters") != {
    "compact": "16px",
    "medium": "24px",
    "expanded": "32px",
    "largeScreen": "48px",
}:
    fail("responsive gutter contract changed")

if data.get("measure") != {
    "prose": "72ch",
    "form": "720px",
    "standard": "1200px",
    "wide": "1600px",
}:
    fail("content measure contract changed")

for density in ("comfortable", "compact", "spacious"):
    if density not in data.get("density", {}):
        fail(f"missing density mode {density}")
if not data["density"]["compact"].get("minimumInteractiveTargetPreserved"):
    fail("compact density must preserve interactive targets")
if not data["density"]["spacious"].get("minimumInteractiveTargetPreserved"):
    fail("spacious density must preserve interactive targets")

requirements = data.get("requirements", {})
for requirement in (
    "safeAreaAware",
    "rootHorizontalOverflowForbidden",
    "densityMustNotReduceAccessibilityTargets",
    "layoutMustSupportLocalizationExpansion",
    "semanticOrderMustMatchFocusOrder",
    "viewportWidthAloneMustNotSelectCompactDensity",
):
    if requirements.get(requirement) is not True:
        fail(f"required rule disabled: {requirement}")

css = CSS.read_text()
for marker in (
    "env(safe-area-inset-left)",
    "overflow-x: clip",
    '[data-glaze-density="compact"]',
    ".glaze-container--prose",
    ".glaze-scroll-x",
    "--glaze-target-coarse: 44px",
):
    if marker not in css:
        fail(f"CSS primitive missing: {marker}")

doc = DOC.read_text()
for marker in (
    "Glaze UI 1.5 Stable",
    "Glaze UI 1.5.0 remains Stable",
    "Density modifies inter-element spacing and padding only",
    "Horizontal scrolling is reserved",
    "Privacy Shield",
    "Wardveil Security",
    "Everkeep",
    "GoreeCloud Mesh",
):
    if marker not in doc:
        fail(f"documentation invariant missing: {marker}")

print("Glaze UI 1.5 layout/spacing/density Stable contract: OK")
