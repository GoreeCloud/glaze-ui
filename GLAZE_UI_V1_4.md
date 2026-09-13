# GLAZE UI V1.4 — Optical Material & Chromatic Depth

**Version:** `1.4.0`  
**Lifecycle:** Official Stable  
**Consumer eligibility:** Eligible for explicit downstream adoption  
**Stable predecessor:** GLAZE UI V1.3 / `1.3.0`  
**Human qualification follow-up:** GLAZE UI V1.4.1

GLAZE UI V1.4 advances the V1.3 Adaptive Resonance foundation with bounded optical material, chromatic depth, composable accessibility requirements, deterministic capability negotiation, browser capability adaptation, resilient fallbacks, and a shared optical runtime for GoreeCloud surfaces.

## Stable release rule

V1.4.0 is a code-complete and automation-qualified Stable release. Its Stable decision is based on implementation, contracts, deterministic runtime behavior, source validation, automated accessibility coverage, compatibility, performance qualification machinery, native-renderer parity evidence machinery, root-shape hardening, semantic color and alpha contracts, icon contracts, and release-authority consistency.

The project owner has explicitly directed that validation requiring human judgment, manual interaction, assistive-technology operation by a human, subjective optical review, representative physical devices, or other human verification does not block V1.4.0. That work is transferred to V1.4.1 and remains explicitly deferred/unverified until performed. It must never be represented as passed V1.4.0 evidence.

## Core principles

1. **Meaning before material.** Readability, state, hierarchy, accessibility, and task completion outrank decorative optical effects.
2. **Capability negotiation is explicit.** Applications request semantic intent; the runtime records accepted, downgraded, substituted, or rejected rendering behavior.
3. **Fallbacks are designed behavior.** Missing translucency, constrained performance, Reduced Transparency, forced colors, or other limitations must resolve deterministically without sacrificing content correctness.
4. **Accessibility requirements compose.** Reduced Transparency, Increased Contrast, Reduced Motion, forced colors, large text, color-vision accommodation, and constrained-performance requirements remain independent when simultaneous.
5. **Privacy is bounded.** Environmental adaptation must not silently become a data collection channel. Protected or privacy-restricted surfaces fail closed for adaptive environmental sampling.
6. **Authority remains separated.** Glaze UI communicates visual and interaction state; it does not grant Wardveil Security, Privacy Shield, GoreeCloud Identity, Everkeep, or application-owned operational authority.
7. **Stable does not auto-certify consumers.** Every GoreeCloud application or service must explicitly adopt V1.4.0 and prove its own applicable platform and release boundary.

## V1.4 Stable architecture

### Optical material foundation

`tokens/glaze-v1.4-optical-material.candidate.json` remains the promoted implementation-source record for optical depth, diffusion, refraction, ambient tint, color bleed, highlight rim, shadow depth, concentration, fallbacks, and component profiles. The `.candidate` suffix records implementation provenance; lifecycle authority comes from the Stable V1.4 wrapper, this contract, `VERSION`, and `registry/lifecycle.json`.

### Semantic optical runtime

`contracts/v1.4/semantic-optical-runtime.candidate.json` and `js/glaze-v1.4-optical-runtime.candidate.mjs` define the promoted implementation layer for semantic material/elevation intent, capability negotiation, accessibility and performance profiles, environmental-sampling boundaries, compositor degradation, and truthful authority separation.

Consumers should enter through `js/glaze-v1.4.0.mjs`, not infer lifecycle status from implementation-stage filenames or metadata objects retained for provenance.

### Composable accessibility

`contracts/v1.4/accessibility-composition.candidate.json` and `js/glaze-v1.4-accessibility-runtime.candidate.mjs` preserve simultaneous accessibility requirements. Reduced Transparency forces a designed solid material; contrast and forced-colors modes suppress optional atmosphere; Reduced Motion suppresses optional material motion; constrained-performance selects the efficient path; large-text and color-vision requirements remain explicit for consuming layout and state-cue policy.

### Browser capability adaptation

`contracts/v1.4/browser-capabilities.candidate.json` and `js/glaze-v1.4-browser-capabilities.candidate.mjs` use bounded local capability and preference detection. They fail closed when evidence is missing and do not require browser identity, device-memory, hardware-concurrency, battery, network, screen-dimension, capture, persistent-storage, telemetry, or analytics access.

### Web rendering

`js/glaze-v1.4-optical-web.candidate.mjs` and `css/glaze-v1.4-optical-runtime.candidate.css` provide the promoted Web implementation. Stable consumers use `js/glaze-v1.4.0.mjs` and `css/glaze-v1.4.0.css` as public entrypoints.

## Stable entrypoints

- `VERSION` — `1.4.0`
- `GLAZE_UI_V1_4.md` — V1.4 Stable contract
- `registry/lifecycle.json` — machine-readable lifecycle authority
- `css/glaze-v1.4.0.css` — Stable Web entrypoint
- `js/glaze-v1.4.0.mjs` — Stable runtime entrypoint
- `acceptance/1.4.0.md` — V1.4 Stable acceptance record
- `GLAZE_UI_V1_4_1_HARDENING.md` — deferred human/manual qualification control plane
- `acceptance/v1.4-deferred-qualification.md` — explicit deferred-evidence boundary

## V1.4.1 deferred qualification

V1.4.1 owns the human-only validation and verification intentionally removed from the V1.4.0 blocking path, including human optical review, manual keyboard and focus traversal, screen-reader/assistive-technology operation, representative workflow review, physical-device/OEM/compositor qualification, native-platform observation, physical-device performance/power observation, and other checks that cannot be truthfully established by deterministic repository automation.

Deferral changes release gating, not truth. Missing human evidence stays missing until V1.4.1 records it.

## Compatibility and rollback

V1.4.0 inherits V1.3.0 as its Stable compatibility baseline. Existing consumers are not migrated automatically. A consumer may remain on V1.3.0 until it explicitly adopts V1.4.0.

If a material V1.4 design-system regression is discovered, V1.3.0 remains the immediately preceding Stable rollback target while the current-line defect is corrected.
