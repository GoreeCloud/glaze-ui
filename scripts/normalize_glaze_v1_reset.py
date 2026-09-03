#!/usr/bin/env python3
"""One-time normalization for the GLAZE UI V1.0 reset branch.

This script intentionally leaves CHANGELOG.md untouched because GoreeCloud
revision-control policy requires the chronological audit trail to remain
preserved. It removes obsolete pre-reset acceptance snapshots from the active
tree and converts inherited 2.2 implementation namespaces into the V1
namespace without claiming production acceptance.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DELETE_PATHS = [
    "acceptance/glaze-motion-0.2-experimental.md",
    "acceptance/glaze-motion-0.3-experimental.md",
    "acceptance/glaze-motion-0.4-experimental.md",
    "acceptance/glaze-motion-0.5-experimental.md",
    "acceptance/glaze-motion-0.6-experimental.md",
]

TEXT_SUFFIXES = {
    ".css", ".html", ".js", ".json", ".kt", ".kts", ".md", ".mjs",
    ".properties", ".py", ".swift", ".xml", ".yaml", ".yml",
}

# Exact path/name references must be converted before the generic namespace
# replacement so candidate suffixes do not survive as broken imports.
EXACT_REPLACEMENTS = {
    "glaze-2.2.foundation.candidate.css": "glaze-v1.foundation.css",
    "glaze-2.2.components.candidate.css": "glaze-v1.components.css",
    "glaze-2.2.components.adaptive.candidate.css": "glaze-v1.components.adaptive.css",
    "glaze-2.2.components.runtime.candidate.css": "glaze-v1.components.runtime.css",
    "glaze-2.2.structure.candidate.css": "glaze-v1.structure.css",
    "glaze-2.2.overlay.candidate.css": "glaze-v1.overlay.css",
    "glaze-2.2.advanced.candidate.css": "glaze-v1.advanced.css",
    "glaze-2.2.visual-refinement.candidate.css": "glaze-v1.visual-refinement.css",
    "glaze-2.2.optical-reachability.candidate.css": "glaze-v1.optical-reachability.css",
    "glaze-2.2.runtime.candidate.mjs": "glaze-v1.runtime.mjs",
    "glaze-2.2.system-interactions.candidate.mjs": "glaze-v1.system-interactions.mjs",
    "Current Stable remains Glaze UI 2.1.0.": "Official version: GLAZE UI V1.0.",
    "Current Stable: 2.1.0": "Official Version: GLAZE UI V1.0",
    "Lifecycle: Candidate (2.2.0-candidate.1)": "Lifecycle: Official reset baseline; production acceptance pending",
    "Lifecycle: Candidate only after exact-head contract + rendered acceptance.": "Lifecycle: Official reset baseline; production acceptance pending.",
}

GENERIC_REPLACEMENTS = {
    "glz22": "glz1",
    "GLZ22": "GLZ1",
    "glaze_2_2": "glaze_v1",
    "GLAZE_2_2": "GLAZE_V1",
    "glaze-ui-2.2": "glaze-ui-v1",
    "GLAZE-UI-2.2": "GLAZE-UI-V1",
    "glaze_ui_2_2": "glaze_ui_v1",
    "GLAZE_UI_2_2": "GLAZE_UI_V1",
    "glaze-2.2": "glaze-v1",
    "GLAZE-2.2": "GLAZE-V1",
    "2.2.0-candidate.1": "1.0.0",
    "2.2.0-candidate": "1.0.0",
}

PRODUCT_VERSION_RE = re.compile(
    r"\bGlaze UI\s+(?:v)?(?:0|1|2)\.\d+(?:\.\d+)?(?:[-._a-z0-9]+)?\b",
    re.IGNORECASE,
)


def normalize(text: str) -> str:
    for old, new in EXACT_REPLACEMENTS.items():
        text = text.replace(old, new)
    for old, new in GENERIC_REPLACEMENTS.items():
        text = text.replace(old, new)
    text = PRODUCT_VERSION_RE.sub("GLAZE UI V1.0", text)
    return text


def main() -> None:
    removed = []
    changed = []

    for rel in DELETE_PATHS:
        path = ROOT / rel
        if path.exists():
            path.unlink()
            removed.append(rel)

    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        rel = path.relative_to(ROOT).as_posix()
        if rel == "CHANGELOG.md" or rel == ".github/workflows/glaze-v1-normalize.yml":
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        original = path.read_text(encoding="utf-8")
        updated = normalize(original)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed.append(rel)

    print(f"removed={len(removed)} changed={len(changed)}")
    for rel in removed:
        print(f"REMOVE {rel}")
    for rel in changed:
        print(f"UPDATE {rel}")


if __name__ == "__main__":
    main()
