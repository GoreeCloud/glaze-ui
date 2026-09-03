#!/usr/bin/env python3
"""Protect the Design Center's mobile-first responsive contract from source regressions."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
CSS = ROOT / "website" / "site.css"
HTML = ROOT / "website" / "index.html"


def main() -> int:
    css = CSS.read_text(encoding="utf-8")
    html = HTML.read_text(encoding="utf-8")
    errors: list[str] = []

    required_css = {
        "normal-flow public header": ".site-header{position:relative;z-index:20",
        "safe-area-aware mobile shell": "padding-inline:max(16px,env(safe-area-inset-left),env(safe-area-inset-right))",
        "compact four-column mobile section navigation": "grid-template-columns:repeat(4,minmax(0,1fr))",
        "48px mobile navigation floor": ".nav-wrap nav a{width:100%;min-width:0;min-height:48px",
        "48px mobile appearance-control floor": ".theme-group button{min-height:48px",
        "mobile hero overrides viewport-fill reach layout": "min-height:0!important;grid-template-columns:1fr!important;grid-template-rows:none!important",
        "mobile hero type has an intentional bounded scale": "font-size:clamp(2.25rem,10.7vw,2.8rem)",
        "hero actions remain a compact two-column mobile group": ".hero .actions{width:100%;display:grid;grid-template-columns:repeat(2,minmax(0,1fr))",
        "buttons center labels instead of stretching text to an edge": ".glaze-button{min-height:48px;display:inline-flex;align-items:center;justify-content:center",
        "System Shell cards remain compact on phones": ".surface-card{min-width:0;min-height:76px",
        "content grids are deliberately single-column on mobile": ".demo-grid,.principle-grid,.gate-grid{display:grid;grid-template-columns:1fr",
        "tablet recomposes rather than shrinking mobile": "@media(min-width:700px)",
        "desktop restores five System Shell surfaces": ".surface-grid{grid-template-columns:repeat(5,minmax(0,1fr))}",
        "reduced-motion support remains present": "@media(prefers-reduced-motion:reduce)",
    }
    for label, marker in required_css.items():
        if marker not in css:
            errors.append(f"Missing responsive contract: {label}")

    required_html = {
        "compact phone brand": '<span class="brand-label-short" aria-hidden="true">GLAZE UI</span>',
        "full desktop brand": '<span class="brand-label-long">GoreeCloud · Design Center · GLAZE UI</span>',
        "viewport safe-area support": 'content="width=device-width,initial-scale=1,viewport-fit=cover"',
    }
    for label, marker in required_html.items():
        if marker not in html:
            errors.append(f"Missing responsive HTML contract: {label}")

    forbidden = {
        "narrow-phone one-column primary navigation": ".nav-wrap nav{grid-row:3;grid-template-columns:1fr}",
        "viewport-filled phone hero inherited from the shared reach layout": "min-height:min(78svh,680px)",
        "unbounded full-width phone action rule": ".actions .glaze-button{width:100%",
    }
    for label, marker in forbidden.items():
        if marker in css:
            errors.append(f"Forbidden mobile regression returned: {label}")

    if errors:
        print("Design Center responsive validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(
        "Design Center mobile-first source validation passed: compact normal-flow navigation, "
        "bounded hero scale, centered 48px controls, compact System Shell cards, safe areas, "
        "and deliberate mobile/tablet/desktop recomposition are protected."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
