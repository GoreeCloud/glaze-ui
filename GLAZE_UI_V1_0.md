# GLAZE UI V1.0 — Official Baseline Contract

**Official product identity:** GLAZE UI V1.0  
**Machine version:** 1.0.0  
**Status:** Official reset baseline; production revalidation required after the reset  
**Repository:** `GoreeCloud/goreecloud-glaze-ui`

GLAZE UI V1.0 is the sole current Glaze UI product version and the only version that may be named as a current GoreeCloud design-system target.

## Design identity

GLAZE UI is GoreeCloud's shared visual and interaction design system. Its defining identity is ergonomic spatial hierarchy, Glaze Material, connected transformation, adaptive expression, accessibility-first interaction, and platform-aware behavior.

**Presentation rule:** Solid where users read or make explicit critical decisions. Glazed where users interact with transient navigation, command, search, control, or feedback chrome.

## V1.0 scope

The V1.0 baseline defines:

- Canvas → Surface → Soft Glaze → Glaze → Deep Glaze → Live Glaze material hierarchy.
- Light, Dark, and Deep Dark appearance modes.
- Calm, Balanced, and Expressive presentation profiles.
- Foundation, Structure, Overlay, Signature, and Intelligence component tiers.
- A 32-component canonical catalog.
- System Shell, Universal Search, Control Center, and workspace interaction patterns.
- Connected Transformation and adaptive density behavior.
- Reduced Motion, Reduced Transparency, Increased Contrast, Forced Colors, RTL, large-text, keyboard, pointer, touch, and assistive-input requirements.
- Minimum 48 px touch-oriented targets and 56 px Touch Assistance / far-view targets where applicable.
- Bounded Glaze use so readable content remains durable and interaction hierarchy remains clear.
- Platform-specific native mapping without replacing native platform semantics.

## Authority and verification

This reset establishes the official product identity and current contract namespace. It does not reuse earlier release identities as V1.0 evidence. Current production-readiness, rendered-reference, native, accessibility, performance, and downstream consumer conformance must be revalidated against the V1.0 namespace and exact post-reset revisions.

No downstream application is upgraded by declaration. Each GoreeCloud application or service must independently adopt V1.0 and satisfy its applicable acceptance requirements.

## Current entrypoints

- Version: `VERSION`
- Official contract: `GLAZE_UI_V1_0.md`
- Lifecycle authority: `registry/lifecycle.json`
- Component catalog: `contracts/components/v1/catalog.json`
- System Shell contract: `contracts/system-shell/glaze-system-shell-v1.json`
- Web entrypoint: `css/glaze-v1.0.0.css`
- Runtime entrypoint: `js/glaze-v1.0.0.mjs`
- Acceptance boundary: `acceptance/v1.0-stable.md`
- V1 validator: `scripts/validate_glaze_v1.py`

Glaze Motion remains a separately governed experimental subsystem unless explicitly incorporated into a future GLAZE UI V1.x contract.
