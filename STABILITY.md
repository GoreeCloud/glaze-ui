# GLAZE UI Stability Contract

**Current Stable authority:** GLAZE UI V1.4 — Optical Material & Chromatic Depth / `1.4.0`  
**Current lifecycle source:** `registry/lifecycle.json`  
**Immediate rollback baseline:** GLAZE UI V1.3 / `1.3.0`

## Stability principles

1. Stable behavior fails closed when required evidence or capabilities are absent.
2. Accessibility, semantic clarity, content correctness, and task completion outrank decorative effects.
3. Reduced Motion, Reduced Transparency, Increased Contrast, Forced Colors, large text/reflow, keyboard, touch, pointer, directional input, and assistive input are first-class requirements where applicable.
4. Durable readable content remains legible when advanced material behavior is unavailable.
5. Exact-revision evidence is required for release claims that depend on that evidence.
6. Recovery uses Git revision history and current-line corrective changes rather than moving or silently rewriting published evidence.
7. Platform-native claims require platform-native evidence.
8. Product-specific readiness remains product-specific; Glaze UI Stable status does not auto-certify consumers.
9. Lifecycle decisions must never manufacture missing evidence.
10. Human/manual/physical-device evidence deferred by release policy remains explicitly unverified until performed.

## V1.4 Stable boundary

V1.4.0 is the automated/code-complete Stable baseline under the project-owner release directive dated 2026-09-13. Its release authority covers the implementation and deterministic repository evidence represented by the exact V1.4 Stable revision.

Human optical review, manual keyboard/focus review, human-operated assistive-technology qualification, subjective presentation review, representative human workflows, physical-device/OEM/compositor qualification, actual native-renderer observation, physical-device production performance/power observation, and other human verification are transferred to V1.4.1. They are not represented as passed V1.4.0 evidence.

## Public entrypoints

- `css/glaze-v1.4.0.css`
- `js/glaze-v1.4.0.mjs`

Implementation-stage `.candidate` files may remain behind these wrappers to preserve provenance. Their filenames or embedded historical lifecycle metadata do not override the aggregate Stable authority established by `VERSION`, `GLAZE_UI_V1_4.md`, `registry/lifecycle.json`, and `acceptance/1.4.0.md`.

## Historical baseline relationship

V1.3.0 remains a supported older Stable target and the immediate rollback baseline for consumers that have not intentionally adopted V1.4.0. Earlier V1.0–V1.2 records remain historical lifecycle evidence and must not be interpreted as the current product target.

Glaze Motion remains separately governed unless an applicable Glaze UI contract explicitly changes that status.
