# GLAZE UI V1.0

GLAZE UI V1.0 is GoreeCloud's official shared visual and interaction design system baseline. **Beauty is a requirement, not a regression risk.**

The sole current product identity is **GLAZE UI V1.0** with machine version **1.0.0**.

## Core rule

**Solid where users read or make explicit critical decisions. Glazed where users interact with transient navigation, command, search, control, or feedback chrome.**

GLAZE UI combines ergonomic spatial hierarchy, Glaze Material, connected transformation, adaptive expression, accessibility-first interaction, privacy-aware presentation, and platform-native behavior.

## Material and interaction hierarchy

The canonical material hierarchy is **Canvas → Surface → Soft Glaze → Glaze → Deep Glaze → Live Glaze**. Durable readable content remains solid. Transient interaction uses bounded Glaze according to role, with restrained depth and no dependence on transparency or effects for basic usability.

V1.0 supports Light, Dark, Deep Dark, Calm, Balanced, Expressive, adaptive density, Reduced Motion, Reduced Transparency, Increased Contrast, Forced Colors, RTL, 200% text, keyboard, pointer, touch, and assistive input. Touch-oriented targets use a 48 px minimum reference floor and 56 px for Touch Assistance / far-view contexts where applicable.

## V1.0 architecture

The V1.0 baseline includes a bounded System Shell and a 32-component catalog across Foundation, Structure, Overlay, Signature, and Intelligence tiers. Universal Search, Control Center, workspace navigation, semantic color, focus, material budgets, and platform-native mapping are part of the design contract where explicitly implemented and validated.

## Reset verification state

V1.0 is the official and only current Glaze UI version. Because the version namespace has been reset, production-readiness and conformance evidence must be regenerated against exact post-reset V1.0 revisions. Earlier release identities are not valid V1.0 evidence and are not current consumer targets.

No downstream GoreeCloud application is upgraded by declaration. Each product must independently adopt V1.0 and complete its required rendered, native, accessibility, platform, performance, and release acceptance.

## Repository layout

- `VERSION` — machine version `1.0.0`.
- `GLAZE_UI_V1_0.md` — official V1.0 contract.
- `registry/lifecycle.json` — current V1 lifecycle authority.
- `contracts/components/v1/catalog.json` — canonical 32-component catalog.
- `contracts/system-shell/glaze-system-shell-v1.json` — V1 System Shell contract.
- `contracts/performance/glaze-v1-performance-budget.json` — V1 performance and Glaze budget.
- `css/glaze-v1.0.0.css` — V1 web entrypoint.
- `js/glaze-v1.0.0.mjs` — V1 runtime entrypoint.
- `acceptance/v1.0-stable.md` — V1 acceptance boundary.
- `scripts/validate_glaze_v1.py` — reset-consistency validator.

## Governance

Git history and the canonical project changelog remain the audit trail required by GoreeCloud revision-control policy. They do not define additional current Glaze UI product versions.

Glaze Motion remains separately Experimental unless a future V1.x contract explicitly changes that status.

## License

MIT. GoreeCloud branding and product identity remain subject to applicable project policies.
