#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = "1.0.0"
ALLOWED_PRODUCT_LABELS = {"1.0", "1.0.0", "v1.0", "v1.0.0"}
TRANSIENT_RESET_FILES = {
    "scripts/normalize_glaze_v1_reset.py",
    "scripts/validate_glaze_v1.py",
    ".github/workflows/glaze-v1-normalize.yml",
}
NONCURRENT_V1_1_CANDIDATE_PATHS = {
    "GLAZE_UI_V1_1_CANDIDATE.md",
    "scripts/promote_glaze_v1_1_stable.py",
    "scripts/promote_glaze_v1_1_bindings.py",
}
NONCURRENT_V1_1_CANDIDATE_PREFIXES = (
    "contracts/v1.1/",
    "tokens/glaze-v1.1-",
    "acceptance/v1.1-",
    "css/glaze-v1.1",
    "reference/v1.1/",
    "scripts/validate_glaze_v1_1_",
    ".github/workflows/glaze-v1.1-",
)
TEXT_SUFFIXES = {
    ".css", ".html", ".js", ".json", ".kt", ".kts", ".md", ".mjs",
    ".properties", ".py", ".swift", ".xml", ".yaml", ".yml",
}


def fail(message: str) -> None:
    raise SystemExit(f"GLAZE UI V1 validation failed: {message}")


def load_json(path: str):
    with (ROOT / path).open(encoding="utf-8") as f:
        return json.load(f)


def is_noncurrent_v1_1_candidate_path(rel: str) -> bool:
    return rel in NONCURRENT_V1_1_CANDIDATE_PATHS or rel.startswith(NONCURRENT_V1_1_CANDIDATE_PREFIXES)


if (ROOT / "VERSION").read_text(encoding="utf-8").strip() != EXPECTED:
    fail("VERSION must be 1.0.0")

lifecycle = load_json("registry/lifecycle.json")
if lifecycle.get("officialProductLabel") != "GLAZE UI V1.0":
    fail("lifecycle official product label mismatch")
if lifecycle.get("currentOfficial") != EXPECTED:
    fail("lifecycle currentOfficial mismatch")

catalog = load_json("contracts/components/v1/catalog.json")
if catalog.get("version") != EXPECTED or catalog.get("componentCount") != 32:
    fail("V1 component catalog mismatch")

consumers = load_json("consumers/registry.json")
if consumers.get("requiredConsumerVersion") != EXPECTED:
    fail("consumer target mismatch")

evidence_schema = load_json("contracts/glaze.conformance-evidence.schema.json")
evidence_target = evidence_schema.get("properties", {}).get("target", {}).get("properties", {})
if evidence_target.get("glaze_version", {}).get("const") != EXPECTED:
    fail("conformance-evidence contract is not bound to V1 product version 1.0.0")
if evidence_schema.get("properties", {}).get("schema_version", {}).get("const") != 2:
    fail("conformance-evidence schema-format revision must remain 2")

required = [
    "README.md",
    "SPECIFICATIONS.md",
    "FEATURES.md",
    "BENEFITS.md",
    "COMPETITIVE-OBJECTIVES.md",
    "BRANDING.md",
    "GLAZE_UI_V1_0.md",
    "css/glaze-v1.0.0.css",
    "js/glaze-v1.0.0.mjs",
    "contracts/system-shell/glaze-system-shell-v1.json",
    "acceptance/v1.0-stable.md",
]
for rel in required:
    if not (ROOT / rel).exists():
        fail(f"missing required V1 artifact: {rel}")

obsolete_acceptance = [
    "acceptance/glaze-motion-0.2-experimental.md",
    "acceptance/glaze-motion-0.3-experimental.md",
    "acceptance/glaze-motion-0.4-experimental.md",
    "acceptance/glaze-motion-0.5-experimental.md",
    "acceptance/glaze-motion-0.6-experimental.md",
]
for rel in obsolete_acceptance:
    if (ROOT / rel).exists():
        fail(f"obsolete pre-reset acceptance artifact remains: {rel}")

# These files directly bind the current product version. Internal subsystem-contract
# revisions, such as icon schema baselines, are deliberately not rewritten as product
# versions.
product_binding_files = [
    ".github/workflows/glaze-ui-evidence-validity.yml",
    "contracts/glaze.conformance-evidence.schema.json",
    "docs/evidence-validity.md",
    "scripts/validate_conformance_evidence.py",
    "scripts/test_validate_conformance_evidence.py",
]
for rel in product_binding_files:
    text = (ROOT / rel).read_text(encoding="utf-8").lower()
    for old in ("2.2.0", "2.1.0", "2.0.0"):
        if old in text:
            fail(f"former Glaze UI product version remains in V1 product binding: {rel}: {old}")

# Active filenames must not retain former Glaze UI release namespaces.
# CHANGELOG.md remains because GoreeCloud revision-control policy requires the
# append-oriented audit trail; historical entries do not define current versions.
filename_forbidden = [
    "glaze-2.2", "glaze_2_2", "glaze-ui-2.2", "glaze_ui_2_2",
    "glaze-2.1", "glaze_2_1", "glaze-ui-2.1", "glaze_ui_2_1",
    "candidate-2.2", "candidate-2.1", "candidate-2.0",
]

content_forbidden = [
    "glz22",
    "glaze-2.2",
    "glaze_2_2",
    "glaze-ui-2.2",
    "glaze_ui_2_2",
    "2.2.0-candidate",
    "current stable: 2.1.0",
    "current stable remains glaze ui 2.1.0",
]
product_version_re = re.compile(
    r"\bglaze ui\s+(v?\d+(?:\.\d+){1,2}(?:[-._a-z0-9]+)?)\b",
    re.IGNORECASE,
)
v1_1_candidate_label_re = re.compile(
    r"^v?1\.1(?:\.0)?(?:-candidate(?:\.\d+)?)?$",
    re.IGNORECASE,
)

for path in ROOT.rglob("*"):
    if not path.is_file() or ".git" in path.parts:
        continue
    rel = path.relative_to(ROOT).as_posix()
    rel_lower = rel.lower()
    if rel == "CHANGELOG.md" or rel in TRANSIENT_RESET_FILES:
        continue
    if any(marker in rel_lower for marker in filename_forbidden):
        fail(f"former release namespace remains in active filename: {rel}")
    if path.suffix.lower() not in TEXT_SUFFIXES:
        continue
    text = path.read_text(encoding="utf-8")
    text_lower = text.lower()
    for marker in content_forbidden:
        if marker in text_lower:
            fail(f"former release namespace remains in active content: {rel}: {marker}")
    candidate_path = is_noncurrent_v1_1_candidate_path(rel)
    for match in product_version_re.finditer(text):
        token = match.group(1).lower()
        if token in ALLOWED_PRODUCT_LABELS:
            continue
        if candidate_path and v1_1_candidate_label_re.fullmatch(token):
            continue
        fail(f"non-V1 Glaze UI product version remains in active content: {rel}: {match.group(0)}")

print("GLAZE UI V1.0 reset contract: OK")
