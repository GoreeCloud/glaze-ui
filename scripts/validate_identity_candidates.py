#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ROUND = ROOT / "branding" / "candidates" / "round-01"
MANIFEST = ROUND / "manifest.json"
REVIEW = ROUND / "REVIEW.md"
IDENTITY = ROOT / "IDENTITY.md"
WEBSITE = ROOT / "website"

ALLOWED_TAGS = {
    "svg", "title", "desc", "defs", "linearGradient", "radialGradient",
    "stop", "g", "path", "rect", "circle", "ellipse", "polygon", "polyline", "line"
}
FORBIDDEN_TEXT = (
    "<script", "javascript:", "data:", "<foreignObject",
    "<image", "<animate", "<set", "<iframe", "<!DOCTYPE", "<!ENTITY"
)
REQUIRED_REVIEW_MODES = {
    "presentation-128px",
    "compact-24px",
    "favicon-16px",
    "light-background",
    "dark-background",
    "monochrome",
}


def fail(message: str) -> None:
    raise SystemExit(f"identity-candidate validation failed: {message}")


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def validate_svg(path: Path) -> str:
    raw = path.read_bytes()
    if len(raw) > 16_384:
        fail(f"{path.name} exceeds 16 KiB review-asset limit")
    text = raw.decode("utf-8")
    lowered = text.lower()
    for marker in FORBIDDEN_TEXT:
        if marker.lower() in lowered:
            fail(f"{path.name} contains forbidden SVG marker {marker!r}")
    try:
        root = ET.fromstring(text)
    except ET.ParseError as exc:
        fail(f"{path.name} is not valid XML: {exc}")
    if local_name(root.tag) != "svg":
        fail(f"{path.name} root is not svg")
    if root.attrib.get("viewBox") != "0 0 64 64":
        fail(f"{path.name} must use review viewBox 0 0 64 64")
    for element in root.iter():
        tag = local_name(element.tag)
        if tag not in ALLOWED_TAGS:
            fail(f"{path.name} uses unapproved SVG element <{tag}>")
        for key, value in element.attrib.items():
            attr = local_name(key)
            if attr.lower().startswith("on"):
                fail(f"{path.name} contains event-handler attribute {attr}")
            if attr in {"href", "xlink:href"} and not value.startswith("#"):
                fail(f"{path.name} contains non-local reference {value!r}")
            if "url(" in value and not re.fullmatch(r".*url\(#[A-Za-z_][\w.-]*\).*", value):
                fail(f"{path.name} contains non-local url() reference")
            if value.startswith(("http://", "https://", "//")):
                fail(f"{path.name} contains remote attribute value {value!r}")
    return git_blob_sha(raw)


def main() -> int:
    if not MANIFEST.is_file():
        fail("round-01 manifest is missing")
    if not REVIEW.is_file():
        fail("round-01 review rubric is missing")

    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if data.get("schema_version") != 2:
        fail("candidate manifest must use schema_version 2")
    if data.get("status") != "unapproved-review-only":
        fail("candidate round must remain unapproved-review-only")
    if data.get("canonical_identity") is not None:
        fail("candidate manifest must not declare a canonical identity")
    if data.get("public_site_integration_allowed") is not False:
        fail("candidate manifest must deny public-site integration")
    if data.get("approval_requires_exact_candidate") is not True:
        fail("candidate approval must require an exact candidate")
    review_modes = data.get("required_review_modes")
    if set(review_modes or []) != REQUIRED_REVIEW_MODES:
        fail("candidate manifest must require the complete review-mode set")
    if data.get("decision_states") != ["pending", "rejected", "approved"]:
        fail("candidate manifest decision states changed unexpectedly")

    candidates = data.get("candidates")
    if not isinstance(candidates, list) or len(candidates) < 3:
        fail("at least three materially different candidates are required")
    names: set[str] = set()
    ids: set[str] = set()
    for item in candidates:
        candidate_id = item.get("id")
        if not isinstance(candidate_id, str) or candidate_id in ids:
            fail("candidate IDs must be unique strings")
        ids.add(candidate_id)
        if item.get("approval") != "pending":
            fail(f"candidate {candidate_id} is not pending")
        filename = item.get("file")
        if not isinstance(filename, str) or filename in names:
            fail("candidate filenames must be unique strings")
        names.add(filename)
        path = ROUND / filename
        if not path.is_file():
            fail(f"manifest candidate file is missing: {filename}")
        actual_blob = validate_svg(path)
        recorded_blob = item.get("git_blob_sha")
        if recorded_blob != actual_blob:
            fail(
                f"candidate {candidate_id} exact-source binding changed: "
                f"manifest {recorded_blob!r}, actual {actual_blob!r}"
            )

    review_text = REVIEW.read_text(encoding="utf-8")
    required_review_markers = (
        "128 px presentation size",
        "24 px compact application-navigation size",
        "16 px favicon-size recognition",
        "Light background",
        "Dark background",
        "Monochrome presentation",
        "Approval must name one exact candidate ID and its recorded Git blob SHA",
        "reject Round 01",
    )
    for marker in required_review_markers:
        if marker not in review_text:
            fail(f"REVIEW.md lost required review boundary: {marker}")

    identity_text = IDENTITY.read_text(encoding="utf-8")
    required_identity_markers = (
        "Pending approved canonical artwork",
        "No icon, logo, favicon, or product mark is approved as canonical",
        "Technical validation is necessary but does not constitute aesthetic approval.",
    )
    for marker in required_identity_markers:
        if marker not in identity_text:
            fail(f"IDENTITY.md lost required approval boundary: {marker}")

    website_text = "\n".join(
        p.read_text(encoding="utf-8", errors="ignore")
        for p in WEBSITE.rglob("*") if p.is_file()
    )
    forbidden_public_refs = ["branding/candidates/", *names, *ids]
    for marker in forbidden_public_refs:
        if marker in website_text:
            fail(f"public website references unapproved identity candidate: {marker}")

    print(
        f"identity candidates: PASS ({len(candidates)} exact-source-bound review-only SVGs; "
        "six review modes required; no public integration)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
