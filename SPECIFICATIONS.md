# GLAZE UI V1.0 — Specifications

## Product identity

- **Official product name:** GLAZE UI V1.0
- **Machine version:** `1.0.0`
- **Repository:** `GoreeCloud/goreecloud-glaze-ui`
- **Lifecycle state:** Official reset baseline; production acceptance pending
- **Authoritative product contract:** `GLAZE_UI_V1_0.md`

GLAZE UI V1.0 is the sole current Glaze UI product version represented by the active repository tree. The reset does not inherit production-Stable or consumer-conformance evidence from any prior product namespace.

## Runtime entry points

- Web CSS: `css/glaze-v1.0.0.css`
- Web JavaScript: `js/glaze-v1.0.0.mjs`
- Design tokens: `tokens/glaze-v1.json`
- Component catalog: `contracts/components/v1/catalog.json`
- System Shell contract: `contracts/system-shell/glaze-system-shell-v1.json`
- Lifecycle registry: `registry/lifecycle.json`
- Consumer registry: `consumers/registry.json`

## Core requirements

GLAZE UI V1.0 provides the GoreeCloud design-system baseline for interface structure, components, states, materials, color, typography, motion, responsive behavior, form factors, accessibility, iconography, workspace navigation, System Shell behavior, evidence presentation, and supported native-platform references.

The active implementation must use the V1 namespace consistently. Former Glaze UI release namespaces must not appear in active filenames, runtime selectors, variables, imports, contracts, examples, tests, or current documentation, except where GoreeCloud revision-control requirements preserve chronological audit history in the canonical changelog or immutable Git history.

## Acceptance boundary

The V1 product identity is authoritative, but production acceptance must be earned against the exact post-reset revision. Required validation includes applicable repository checks, rendered-reference review, accessibility checks, interaction checks, performance checks, native-platform checks, and human visual review. Downstream applications remain independently conformance-gated.
