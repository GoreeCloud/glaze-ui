#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "EVIDENCE_PRESENTATION.md"
TOKENS = ROOT / "tokens" / "evidence-presentation.json"
CSS = ROOT / "css" / "glaze.evidence.css"
REFERENCE = ROOT / "reference" / "candidate-1.6-evidence.html"
STATUS = ROOT / "COMPONENT_STATUS.md"


def fail(message: str) -> None:
    raise SystemExit(f"evidence presentation validation failed: {message}")


for path in (DOC, TOKENS, CSS, REFERENCE, STATUS):
    if not path.is_file():
        fail(f"missing {path.relative_to(ROOT)}")

try:
    data = json.loads(TOKENS.read_text())
except Exception as exc:
    fail(f"invalid token JSON: {exc}")

if data.get("glaze_ui", {}).get("candidate") != "1.6":
    fail("candidate must remain 1.6")
if data.get("glaze_ui", {}).get("lifecycle") != "candidate":
    fail("evidence presentation must remain Candidate until promotion")
if data.get("glaze_ui", {}).get("stable_consumer_target") != "1.5.0":
    fail("current Stable consumer target must remain 1.5.0")

for family in ("freshness_states", "transport_states"):
    values = data.get(family, {})
    if not values:
        fail(f"missing {family}")
    for name, item in values.items():
        if item.get("positive_domain_truth") is not False:
            fail(f"{family}.{name} must never imply positive domain truth")

systems = data.get("authority_systems", {})
for system in ("wardveil-security", "privacy-shield", "everkeep", "goreecloud-mesh", "glaze-ui"):
    if system not in systems:
        fail(f"missing authority system {system}")

html = REFERENCE.read_text()
for marker in (
    "Glaze UI 1.6 Candidate",
    "Glaze UI 1.5.0 remains the current Stable consumer target",
    "Wardveil Security",
    "Privacy Shield",
    "Everkeep",
    "GoreeCloud Mesh",
    'data-freshness="current"',
    'data-freshness="expired"',
    'data-freshness="unknown"',
    'data-transport="available"',
    'data-transport="unavailable"',
    "Data use denied",
    "Restore verification failed",
    "Freshness is not success",
    "different domains",
):
    if marker not in html:
        fail(f"reference invariant missing: {marker}")

if "All safe" in html or "Everything is protected" in html:
    fail("reference must not collapse distinct authority domains into generic safety")

css = CSS.read_text()
for marker in (
    ".glaze-evidence-card",
    ".glaze-evidence-chip[data-freshness]",
    ".glaze-evidence-chip[data-transport]",
    "@media (prefers-reduced-motion: reduce)",
    "@media (prefers-reduced-transparency: reduce)",
    "@media (forced-colors: active)",
):
    if marker not in css:
        fail(f"candidate CSS invariant missing: {marker}")

if "current/available must never inherit success/protected styling" not in css:
    fail("candidate CSS must document neutral current/available transport semantics")

status = STATUS.read_text()
if "Evidence presentation and authority surfaces | Candidate" not in status:
    fail("component lifecycle registry must keep evidence presentation Candidate")

doc = DOC.read_text()
for marker in (
    "Freshness describes evidence timing, not domain success.",
    "Transport availability must not be rendered as protection",
    "Glaze UI presents evidence; it does not create evidence.",
):
    if marker not in doc:
        fail(f"documentation invariant missing: {marker}")

print("Glaze UI 1.6 evidence presentation Candidate contract: OK")
