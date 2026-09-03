#!/usr/bin/env python3
"""Validate current GLAZE UI V1.0 evidence-presentation authority and retained 1.6 rendered evidence."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "EVIDENCE_PRESENTATION.md"
TOKENS = ROOT / "tokens" / "evidence-presentation.json"
SCHEMA = ROOT / "contracts" / "glaze.evidence-presentation.schema.json"
CSS = ROOT / "css" / "glaze.evidence.css"
REFERENCE = ROOT / "reference" / "candidate-1.6-evidence.html"
ACCEPTANCE = ROOT / "reference" / "candidate-1.6-evidence-acceptance.html"
RENDERED_VALIDATOR = ROOT / "scripts" / "validate_candidate_1_6_evidence_rendered.py"
ACCEPTANCE_RECORD = ROOT / "acceptance" / "1.6.0.md"
CONSUMER = ROOT / "reference" / "mesh-evidence-consumer.mjs"
CONSUMER_TEST = ROOT / "tests" / "mesh-evidence-consumer.test.mjs"
STATUS = ROOT / "COMPONENT_STATUS.md"
VERSION = ROOT / "VERSION"


def fail(message: str) -> None:
    raise SystemExit(f"evidence presentation validation failed: {message}")


for path in (
    DOC,
    TOKENS,
    SCHEMA,
    CSS,
    REFERENCE,
    ACCEPTANCE,
    RENDERED_VALIDATOR,
    ACCEPTANCE_RECORD,
    CONSUMER,
    CONSUMER_TEST,
    STATUS,
    VERSION,
):
    if not path.is_file():
        fail(f"missing {path.relative_to(ROOT)}")

try:
    data = json.loads(TOKENS.read_text())
    schema = json.loads(SCHEMA.read_text())
except Exception as exc:
    fail(f"invalid contract JSON: {exc}")

if VERSION.read_text().strip() != "2.2.0":
    fail("repository VERSION must be the current 2.2.0 Stable target")
# The 2.1 field records the last dedicated Candidate mapping that extended the
# original 1.6 capability. It is provenance, not the current release authority.
if data.get("glaze_ui", {}).get("candidate") != "2.1":
    fail("historical evidence-presentation Candidate mapping must remain GLAZE UI V1.0")
if data.get("glaze_ui", {}).get("lifecycle") != "stable":
    fail("evidence presentation must remain Stable")
if data.get("glaze_ui", {}).get("introduced_in") != "1.6.0":
    fail("historical evidence presentation introduction must remain 1.6.0")
if data.get("glaze_ui", {}).get("stable_consumer_target") != "2.2.0":
    fail("current evidence presentation Stable consumer target must be 2.2.0")
if data.get("glaze_ui", {}).get("release") != "2.2.0":
    fail("current evidence presentation release must be 2.2.0")

for family in ("freshness_states", "transport_states"):
    values = data.get(family, {})
    if not values:
        fail(f"missing {family}")
    for name, item in values.items():
        if item.get("positive_domain_truth") is not False:
            fail(f"{family}.{name} must never imply positive domain truth")

systems = data.get("authority_systems", {})
for system in (
    "wardveil-security",
    "privacy-shield",
    "everkeep",
    "goreecloud-mesh",
    "goreecloud-identity",
    "glaze-ui",
):
    if system not in systems:
        fail(f"missing authority system {system}")

identity_domains = set(systems["goreecloud-identity"].get("domains", []))
expected_identity_domains = {
    "identity",
    "authentication",
    "authorization",
    "accounts",
    "devices",
    "credentials",
    "sessions",
    "delegated-authority",
}
if identity_domains != expected_identity_domains:
    fail("GoreeCloud Identity presentation domains drifted from the canonical authority boundary")

schema_authorities = set(schema.get("properties", {}).get("authority", {}).get("enum", []))
if not set(systems).issubset(schema_authorities):
    fail("evidence schema authority enum must cover every presentation authority system")

# The 1.6 rendered artifacts are immutable historical promotion evidence. Their
# embedded version/lifecycle wording is intentionally preserved and must not be
# rewritten to manufacture modern provenance.
html = REFERENCE.read_text()
for marker in (
    "GLAZE UI V1.0 Candidate",
    "GLAZE UI V1.0 remains the current Stable consumer target",
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
        fail(f"historical 1.6 reference invariant missing: {marker}")

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
        fail(f"evidence CSS invariant missing: {marker}")

if "current/available must never inherit success/protected styling" not in css:
    fail("evidence CSS must document neutral current/available transport semantics")

acceptance = ACCEPTANCE.read_text()
for marker in (
    "GLAZE UI V1.0 Candidate evidence acceptance",
    "current Privacy Shield denial example missing",
    "current Everkeep negative recovery example missing",
    "generic aggregate safety verdict present",
    "200% text scale caused horizontal root overflow",
    "TV disclosure target did not retain 56px far-view floor",
    "forced-colors evidence distinction rendered",
):
    if marker not in acceptance:
        fail(f"historical rendered evidence acceptance invariant missing: {marker}")

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
        fail(f"historical rendered evidence validator missing required case: {marker}")

consumer = CONSUMER.read_text()
for marker in (
    "mesh.evidence.read",
    "Authorization",
    "wardveil-security",
    "privacy-shield",
    "everkeep",
    "goreecloud-identity",
    '"authentication"',
    "PRODUCER_AUTHORITY_DOMAINS",
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
    "identity_score",
    "trust_score",
):
    if prohibited in consumer:
        fail(f"Mesh consumer must not create combined domain truth: {prohibited}")

consumer_test = CONSUMER_TEST.read_text()
for marker in (
    'producer: "goreecloud-identity"',
    'authority_domain: "authentication"',
    "rejects cross-domain producer authority escalation before presentation",
):
    if marker not in consumer_test:
        fail(f"Identity presentation regression missing: {marker}")

status = STATUS.read_text()
if "Evidence presentation and authority surfaces | Stable" not in status:
    fail("component lifecycle registry must mark evidence presentation Stable")
if "Glaze UI **2.2.0 is the current Stable consumer target**" not in status:
    fail("component lifecycle registry must identify 2.2.0 as current Stable target")

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
    "Identity Center",
    "GoreeCloud Identity",
    "Glaze UI **2.2.0** Stable consumer target",
    "Current 2.2 acceptance boundary",
    "Reduced Transparency / effective Solid",
    "System Glaze budget",
):
    if marker not in doc:
        fail(f"documentation invariant missing: {marker}")

acceptance_record = ACCEPTANCE_RECORD.read_text()
for marker in (
    "Stable version: `1.6.0`",
    "Previous Stable baseline: `1.5.0`",
):
    if marker not in acceptance_record:
        fail(f"historical 1.6 acceptance record missing lifecycle invariant: {marker}")

print("GLAZE UI V1.0 evidence presentation contract validated; retained 1.6 rendered provenance and producer authority remain intact")
