#!/usr/bin/env python3
"""Synchronize current-version bindings during the atomic GLAZE UI V1.1 promotion."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def rewrite(path: str, replacements: tuple[tuple[str, str], ...]) -> None:
    target = ROOT / path
    text = target.read_text(encoding="utf-8")
    original = text
    for old, new in replacements:
        text = text.replace(old, new)
    if text == original:
        raise SystemExit(f"expected current-version bindings were not found in {path}")
    target.write_text(text, encoding="utf-8")


def main() -> int:
    product_replacements = (
        ("GLAZE UI V1.0", "GLAZE UI V1.1"),
        ("1.0.0", "1.1.0"),
    )
    for path in (
        "scripts/validate_conformance_evidence.py",
        "scripts/test_validate_conformance_evidence.py",
        "docs/evidence-validity.md",
        ".github/workflows/glaze-ui-evidence-validity.yml",
        "ADOPTION.md",
        "CONFORMANCE.md",
        "BENEFITS.md",
    ):
        rewrite(path, product_replacements)

    features = ROOT / "FEATURES.md"
    text = features.read_text(encoding="utf-8")
    text = text.replace("# GLAZE UI V1.0 — Features", "# GLAZE UI V1.1 — Features")
    text = text.replace(
        "This file describes capabilities present in the V1 reset source tree or required by its active contracts. Production-Stable status and downstream adoption remain subject to fresh V1 acceptance evidence.",
        "This file describes capabilities present in the current Stable V1.1 source tree or required by its active contracts. Downstream adoption and application production acceptance remain subject to fresh consumer-specific evidence.",
    )
    text = text.replace(
        "The repository includes automated validation for the V1 reset contract,",
        "The repository includes automated validation for the current V1.1 Stable contract, source-pinned optical regression, bounded Android release evidence,",
    )
    features.write_text(text, encoding="utf-8")

    print("Synchronized current V1.1 conformance, adoption, evidence-validity, benefits, and feature bindings.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
