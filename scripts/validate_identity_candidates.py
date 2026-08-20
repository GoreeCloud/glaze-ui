#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ROUND = ROOT / "branding" / "candidates" / "round-01"
MANIFEST = ROUND / "manifest.json"
IDENTITY = ROOT / "IDENTITY.md"
WEBSITE = ROOT / "website"

ALLOWED_TAGS = {
    "svg", "title", "desc", "defs", "linearGradient", "radialGradient",
    "stop", "g", "path", "rect", "circle", "ellipse", "polygon", "polyline", "line"
}
FORBIDDEN_TEXT = (
    "<script", "javascript:", "data:", "http://", "https://", "<foreignObject",
    "<image", "<animate", "<set", "<iframe", "<!DOCTYPE", "<!ENTITY"
)


def fail(message: str) -> None:
    raise SystemExit(f"identity-candidate validation failed: {message}")


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def validate_svg(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if len(text.encode("utf-8")) > 16_384:
        fail(f"{path.name} exceeds 16 KiB review-asset limit")
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


def main() -> int:
    if not MANIFEST.is_file():
        fail("round-01 manifest is missing")
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if data.get("status") != "unapproved-review-only":
        fail("candidate round must remain unapproved-review-only")
    if data.get("canonical_identity") is not None:
        fail("candidate manifest must not declare a canonical identity")
    if data.get("public_site_integration_allowed") is not False:
        fail("candidate manifest must deny public-site integration")
    candidates = data.get("candidates")
    if not isinstance(candidates, list) or len(candidates) < 3:
        fail("at least three materially different candidates are required")
    names: set[str] = set()
    for item in candidates:
        if item.get("approval") != "pending":
            fail(f"candidate {item.get('id')} is not pending")
        filename = item.get("file")
        if not isinstance(filename, str) or filename in names:
            fail("candidate filenames must be unique strings")
        names.add(filename)
        path = ROUND / filename
        if not path.is_file():
            fail(f"manifest candidate file is missing: {filename}")
        validate_svg(path)

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
    forbidden_public_refs = ["branding/candidates/", *names]
    for marker in forbidden_public_refs:
        if marker in website_text:
            fail(f"public website references unapproved identity candidate: {marker}")

    print(f"identity candidates: PASS ({len(candidates)} review-only SVGs; no public integration)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
