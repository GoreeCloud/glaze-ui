#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "EVIDENCE_PRESENTATION.md"
TOKENS = ROOT / "tokens" / "evidence-presentation.json"
CSS = ROOT / "css" / "glaze.evidence.css"
REFERENCE = ROOT / "reference" / "candidate-1.6-evidence.html"
ACCEPTANCE = ROOT / "reference" / "candidate-1.6-evidence-acceptance.html"
RENDERED_VALIDATOR = ROOT / "scripts" / "validate_candidate_1_6_evidence_rendered.py"
ACCEPTANCE_RECORD = ROOT / "acceptance" / "1.6.0.md"
CONSUMER = ROOT / "reference" / "mesh-evidence-consumer.mjs"
CONSUMER_TEST = ROOT / "tests" / "mesh-evidence-consumer.test.mjs"
STATUS = ROOT / "COMPONENT_STATUS.md"


def fail(message: str) -> None:
    raise SystemExit(f"evidence presentation validation failed: {message}")


for path in (
    DOC,
    TOKENS,
    CSS,
    REFERENCE,
    ACCEPTANCE,
    RENDERED_VALIDATOR,
    ACCEPTANCE_RECORD,
    CONSUMER,
    CONSUMER_TEST,
    STATUS,
):
    if not path.is_file():
        fail(f"missing {path.relative_to(ROOT)}")

try:
    data = json.loads(TOKENS.read_text())
except Exception as exc:
    fail(f"invalid token JSON: {exc}")

if data.get("glaze_ui", {}).get("candidate") != "1.6":
    fail("candidate must remain 1.6")
if data.get("glaze_ui", {}).get("lifecycle") != "stable":
    fail("evidence presentation must be Stable after 1.6.0 promotion")
if data.get("glaze_ui", {}).get("stable_consumer_target") != "1.6.0":
    fail("evidence presentation Stable consumer target must be 1.6.0")

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
    'data-glaze-candidate="1.6-evidence"',
    'data-authority-domain="security"',
    'data-authority-domain="privacy"',
    'data-authority-domain="continuity"',
    'data-authority-domain="coordination"',
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
    "textScale",
    "reduced-transparency",
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
    'data-glaze-form-factor="tv"',
    'data-glaze-reduced-transparency="true"',
    "@media (prefers-reduced-motion: reduce)",
    "@media (prefers-reduced-transparency: reduce)",
    "@media (forced-colors: active)",
):
    if marker not in css:
        fail(f"candidate CSS invariant missing: {marker}")

if "current/available must never inherit success/protected styling" not in css:
    fail("candidate CSS must document neutral current/available transport semantics")

acceptance = ACCEPTANCE.read_text()
for marker in (
    "Glaze UI 1.6 Candidate evidence acceptance",
    "current Privacy Shield denial example missing",
    "current Everkeep negative recovery example missing",
    "generic aggregate safety verdict present",
    "200% text scale caused horizontal root overflow",
    "TV disclosure target did not retain 56px far-view floor",
    "forced-colors evidence distinction rendered",
):
    if marker not in acceptance:
        fail(f"rendered evidence acceptance invariant missing: {marker}")

rendered_validator = RENDERED_VALIDATOR.read_text()
for marker in (
    '(390, 844, "mobile")',
    '(820, 1180, "tablet")',
    '(1280, 900, "desktop")',
    '(1600, 1000, "wide-desktop")',
    '(1920, 1080, "tv")',
    'mode="reduced-motion"',
    'mode="reduced-transparency"',
    'mode="forced-colors"',
    "text_scale=2",
):
    if marker not in rendered_validator:
        fail(f"rendered evidence validator missing required case: {marker}")

consumer = CONSUMER.read_text()
for marker in (
    "mesh.evidence.read",
    "Authorization",
    "wardveil-security",
    "privacy-shield",
    "everkeep",
    "Transport state is not domain truth.",
    "no overall domain verdict is created",
    "Mesh evidence transport is unavailable",
):
    if marker not in consumer:
        fail(f"Mesh consumer invariant missing: {marker}")
for prohibited in (
    "overall_safety",
    "overallSafety",
    "protection_score",
    "privacy_score",
    "recovery_score",
):
    if prohibited in consumer:
        fail(f"Mesh consumer must not create combined domain truth: {prohibited}")

status = STATUS.read_text()
if "Evidence presentation and authority surfaces | Stable" not in status:
    fail("component lifecycle registry must mark evidence presentation Stable")

doc = DOC.read_text()
for marker in (
    "Freshness describes evidence timing, not domain success.",
    "Transport availability must not be rendered as protection",
    "Glaze UI presents evidence; it does not create evidence.",
    "## Consumer mapping examples",
    "Security Center",
    "Privacy Center",
    "Continuity Center",
    "Mesh Center",
    "200% text-scaling/reflow validation",
):
    if marker not in doc:
        fail(f"documentation invariant missing: {marker}")

acceptance_record = ACCEPTANCE_RECORD.read_text()
for marker in (
    "Stable version: `1.6.0`",
    "Previous Stable baseline: `1.5.0`",
    "Stable version: `1.6.0`",
):
    if marker not in acceptance_record:
        fail(f"1.6 acceptance record missing lifecycle invariant: {marker}")

print("Glaze UI 1.6 evidence presentation Candidate contract: OK")
