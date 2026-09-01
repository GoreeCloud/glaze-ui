#!/usr/bin/env python3
"""Protect the public Design Center responsive integration from layout regressions."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
CSS = ROOT / "website" / "site.css"


def main() -> int:
    errors: list[str] = []
    css = CSS.read_text(encoding="utf-8")

    required = {
        "public header remains in normal document flow": ".site-header{position:relative;inset-block-start:auto}",
        "tablet navigation becomes a two-column touch grid": "@media(max-width:820px){.nav-wrap{grid-template-columns:1fr auto}.nav-wrap nav{display:grid;grid-template-columns:repeat(2,minmax(0,1fr))",
        "phone navigation retains two touch columns": "@media(max-width:640px){html{scroll-padding-top:24px}.nav-wrap{padding-block:10px}.nav-wrap nav{margin-inline:0;padding:0;grid-template-columns:repeat(2,minmax(0,1fr))",
        "narrow phone navigation becomes one column": "@media(max-width:440px){.nav-wrap{grid-template-columns:1fr}.theme-group{justify-self:start}.nav-wrap nav{grid-row:3;grid-template-columns:1fr}",
        "material surfaces collapse to one column on phones": ".surface-grid,.principle-grid,.demo-grid,.gate-grid{grid-template-columns:1fr}",
        "tablet material surfaces recompose instead of shrinking desktop": ".surface-grid{grid-template-columns:repeat(2,minmax(0,1fr))}",
        "navigation links meet the 48px general interaction floor": ".nav-wrap nav a{width:100%;min-height:48px",
        "phone actions become full width": ".actions .glaze-button{width:100%;justify-content:center}",
        "public reference anchors do not reserve sticky-header space": "html{scroll-padding-top:24px}",
    }
    for label, marker in required.items():
        if marker not in css:
            errors.append(f"Missing responsive contract: {label}")

    sticky = css.rfind(".site-header{position:sticky")
    normal_flow = css.rfind(".site-header{position:relative;inset-block-start:auto}")
    if sticky >= 0 and normal_flow <= sticky:
        errors.append("Final Design Center cascade does not override sticky public navigation with normal-flow navigation")

    if errors:
        print("Design Center responsive validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("Design Center responsive layout validation passed: normal-flow navigation, 48px touch targets, deliberate tablet/phone grids, single-column material content, and full-width narrow actions are protected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
