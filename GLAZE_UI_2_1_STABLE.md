# Glaze UI 2.1 — Enforced Stable Design Contract

**Lifecycle status:** Stable  
**Stable semantic version:** 2.1.0  
**Previous Stable implementation baseline:** Glaze UI 2.0.0  
**Promoted from:** Glaze UI 2.1.0-candidate.1  
**Human Visual Excellence:** Accepted 2026-08-30

Glaze UI 2.1 is the current GoreeCloud design-system contract once the canonical `VERSION` is promoted to `2.1.0` and the exact promotion revision passes CI.

The governing sentence remains:

> **Make interaction feel tangible.**

The structural rule remains:

> **Content is solid. Interaction is glazed.**

And connected interaction must preserve the rule:

> **Nothing teleports.**

## Stable material hierarchy

The Stable hierarchy is:

**Canvas / Surface / Soft Glaze / Glaze / Deep Glaze / Live Glaze**

Glaze is concentrated in navigation, controls, toolbars, command surfaces, live activity, transient interaction and other interaction chrome. Reading and durable content planes remain solid by default.

2.1 strengthens the perceptual glass character of interaction chrome while preserving semantic color coding. Selected controls retain GoreeCloud accent tint; Live Glaze retains semantic positive/accent tint; failure, attention, protection, offline and other semantic states remain distinguishable by text, shape and state vocabulary rather than color alone.

Reduced Transparency / effective Solid, Forced Colors, Increased Contrast, Reduced Motion, Large Text and Touch Assistance remain authoritative renderings. Accessibility never becomes a decorative exception path.

## Stable 2.1 additions over 2.0

Glaze UI 2.1 promotes the following system-level capabilities:

- deterministic Material Budgets and performance degradation;
- machine-readable material, component and accessibility-resolution contracts;
- Clear / Balanced / Solid Material Clarity resolution;
- density profiles including Comfortable, Standard, Compact and Far View;
- accessibility precedence for Reduced Transparency, Forced Colors, Reduced Motion, Increased Contrast, 200% Large Text and Touch Assistance;
- canonical Settings, Files, Search/Command, Communication/Live Activity, Media Playback and Resilience reference flows;
- explicit exceptional-state vocabulary and recovery presentation;
- source-pinned screenshot pixel regression with immutable provenance;
- a bounded native Android handheld reference and emulator acceptance gate;
- refined color-coded glass presentation accepted through human Visual Excellence review.

## Versioned Stable entrypoints

For the 2.1 web reference layer:

- `css/glaze-2.1.0.css`
- `js/glaze-2.1.0.mjs`

The promoted Candidate source remains preserved for provenance:

- `css/glaze-2.1.reference.css`
- `css/glaze-2.1.visual-excellence.css`
- `js/glaze-2.1.candidate.mjs`
- `GLAZE_UI_2_1_CANDIDATE.md`
- `acceptance/2.1-candidate.md`

Native consumers map the Stable contracts to platform-native controls and APIs; they are not required to embed the web reference layer.

## Human Visual Excellence evidence

The refined presentation baseline is revision:

`5b46903c18660ae78e7f1aaea39a93136efacda7`

Baseline artifact:

- workflow run `33327634493`
- artifact `9736700947`
- digest `sha256:ba7385928fbd0a9768adc73d7ec535dfd122c27978a2c16a49cd87df680eb75b`

The approved exact-head Candidate revision is:

`a21601691dc412baa6a889533d6fa5b3a7996dc2`

Its exact-head web evidence is artifact `9736839184`, digest `sha256:82cb14f664478e23bb9c5ab9abd666e51e0ee38f6943d7f53a592d3440c6db05`. Its Android emulator evidence is artifact `9736880167`, digest `sha256:08540546ffd8289441b1fb6018b4732333e056ce8ecf9b6b1a38f3bf6d3a93d0`.

The human decision was explicitly **Approve Visual Excellence** on 2026-08-30.

## Stable promotion and rollback boundary

2.1 Stable promotion requires the final promotion revision to pass the repository's exact-revision CI and 2.1 web/native acceptance gates. The release tag becomes the immutable final revision anchor after merge.

Rollback returns the canonical Stable pointer to the preserved Glaze UI 2.0.0 implementation and its historical contract; Candidate evidence is never deleted to manufacture a cleaner history.

## Consumer boundary

**No downstream application is promoted by declaration.**

When 2.1.0 becomes current Stable, all audited GoreeCloud user-facing consumers receive `2.1.0` as their required target. Existing 2.0 and earlier evidence becomes migration input. A consumer becomes production eligible only after its own repository-local exact-revision validation and application-specific rendered, accessibility, native or real-device acceptance as applicable.

Glaze Motion remains separately governed and Experimental. Glaze UI 2.1 does not promote it.
