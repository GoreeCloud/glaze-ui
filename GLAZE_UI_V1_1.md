# GLAZE UI V1.1 — Optical Refinement Release Contract

**Product identity:** GLAZE UI V1.1  
**Machine version:** 1.1.0  
**Lifecycle:** Release Candidate until the exact release revision satisfies the Stable acceptance boundary  
**Repository:** `GoreeCloud/goreecloud-glaze-ui`

GLAZE UI V1.1 is the governed incremental refinement of the V1 design language. It preserves V1 semantic roles, accessibility requirements, material hierarchy, truth boundaries, platform-native mapping, and bounded Glaze use while strengthening optical quality and GoreeCloud visual identity.

V1.0 remains the current official reset baseline until V1.1 is promoted through the governed Stable release process. A branch, pull request, passing source check, rendered screenshot, or version-string change alone does not make V1.1 current or Stable.

## V1.1 defining refinement

V1.1 adds and governs:

- A unified optical lighting model with directional edge light, restrained internal highlight, lower-edge occlusion, and depth-dependent shadows.
- Deep Teal + Soft Amber as the primary non-semantic atmospheric identity over blue-black graphite neutrals.
- Environmental Color Memory through a bounded local CSS custom-property input that never replaces semantic color.
- A coordinated curvature grammar for micro, control, container, hero, and capsule geometry.
- Explicit depth levels 0 through 6.
- Expanded typography roles for display, title, heading, body, UI, caption, and numeric content.
- Comfortable, Standard, Productive, and Immersive optical-density profiles.
- Bounded interaction microphysics with reduced-motion fallbacks.
- Adaptive Glaze tinting and constrained-performance fallbacks.
- Independent Dark and Deep Dark atmospheric composition.
- Functional Aura categories implemented with restrained teal, amber, dual, or neutral environmental fields.
- Versioned V1.1 web and runtime entrypoints.
- Release-specific performance, visual-regression, accessibility, and exact-revision validation gates.

## Atmospheric identity

The V1.1 atmospheric palette is environmental presentation, not status meaning.

### Environmental neutrals

- Canvas Black: `#081016`
- Deep Graphite: `#101A20`
- Slate Graphite: `#18252B`

### Deep Teal family

- Deep Teal: `#0F6B6F`
- Mineral Teal: `#1C8A8D`
- Soft Aqua: `#8FD6D2`

### Soft Amber family

- Soft Amber: `#D9A35F`
- Champagne Gold: `#E7C78A`
- Warm Glow: `#F2D7A6`

Muted Coral may be used only as a rare expressive accent. It is not a third primary Glaze color and is not a default semantic state color.

Semantic roles including success, information, warning, critical, destructive, privacy, security, online, offline, syncing, protected, restricted, unavailable, focus, and selection remain governed independently from atmospheric color.

## Accessibility and resilience

Atmosphere, transparency, blur, Aura, environmental tint, and nonessential motion must gracefully reduce or disappear under applicable Reduced Transparency, Reduced Motion, Increased Contrast, Forced Colors, grayscale/color-vision accommodation, constrained-performance, and unsupported-effect conditions.

Meaning, hierarchy, focus, selection, readable content, interaction boundaries, critical decisions, and protected system states must remain understandable without atmospheric effects.

## Performance boundary

The V1.1 optical layer is governed by `contracts/performance/glaze-v1-performance-budget.json`. Expensive presentation is bounded; nested backdrop blur remains prohibited; one dominant Glaze panel and no more than three small floating Glaze controls remain the default material budget.

## Visual acceptance boundary

The V1.1 Design Center and reference surfaces are governed by `contracts/regression/visual-baselines-v1.json` and exact-revision rendered validation. Mobile remains the highest-priority website visual acceptance surface, with desktop/tablet and accessibility-mode checks retained as applicable.

Automated screenshots support visual review but do not manufacture acceptance. Stable promotion requires the exact release revision to satisfy the repository's applicable source, rendered, accessibility, interaction, performance, native-reference, documentation, and release-validation requirements.

## Entrypoints

- Version: `VERSION`
- Release contract: `GLAZE_UI_V1_1.md`
- Lifecycle authority: `registry/lifecycle.json`
- Web entrypoint: `css/glaze-v1.1.0.css`
- Optical/atmospheric layer: `css/glaze-v1.1.optical.css`
- Runtime entrypoint: `js/glaze-v1.1.0.mjs`
- Optical runtime controls: `js/glaze-v1.1.runtime.mjs`
- Performance budget: `contracts/performance/glaze-v1-performance-budget.json`
- Visual regression contract: `contracts/regression/visual-baselines-v1.json`
- Acceptance boundary: `acceptance/v1.1-stable.md`
- Current V1-series validator: `scripts/validate_glaze_v1.py`

Glaze Motion remains separately governed as Experimental. V1.1 uses bounded CSS/runtime motion behavior defined by the Glaze UI contract and does not promote or silently incorporate the separately governed Glaze Motion subsystem.
