# GLAZE UI V1.1 — Specification-Stable Candidate

Status: **Specification-Stable Candidate**  
Candidate version: **1.1.0-candidate.1**  
Current official target: **GLAZE UI V1.0 / 1.0.0**

This document records the repository-side implementation contract for the proposed Glaze UI V1.1 optical refinement. It does not promote V1.1 to the current product identity, Stable release, Production Stable implementation, or downstream conformance target.

## Purpose

V1.1 is an incremental optical refinement of the V1 generation. It sharpens lighting, curvature, atmosphere, hierarchy, density presentation, state rendering, and visual acceptance while preserving V1 semantics, accessibility, material restraint, form-factor requirements, and source-of-truth boundaries.

The defining shared atmosphere is **Deep Teal + Soft Amber** over neutral graphite structure.

## Frozen boundaries

V1.1 does not, by this candidate:

- promote Glaze Motion from its separately governed Experimental lifecycle;
- expand the canonical V1 component catalog;
- add or reinterpret protected security, privacy, identity, resilience, coordination, connectivity, or status semantics;
- allow default nested backdrop blur or unbounded decorative refraction;
- require environmental content sampling;
- make Muted Coral a canonical V1.1 atmospheric color;
- change the current `VERSION` or lifecycle records.

## Machine contracts

The candidate is defined by:

- `contracts/v1.1/optical-refinement.candidate.json`
- `tokens/glaze-v1.1-atmosphere.candidate.json`
- `scripts/validate_glaze_v1_1_candidate.py`
- `acceptance/v1.1-specification-candidate.md`

Current V1 contracts remain authoritative until a separately governed V1.1 release promotion occurs.

## Resolution order

V1.1 presentation resolves in this order:

1. producer-authoritative protected semantic meaning;
2. Forced Colors;
3. Reduced Motion;
4. Reduced Transparency;
5. Increased Contrast and boundary visibility;
6. Large Text, 200% text scaling, Touch Assistance, and accessibility geometry;
7. material clarity and platform capability;
8. V1.1 atmosphere, application identity, and personalization.

Atmosphere always yields before semantics, focus, accessibility, or hierarchy.

## Material compatibility

V1.1 preserves the V1 structural material baseline. Functional glass remains bounded by the current material contract, nested backdrop stacks remain disallowed by default, durable readable content does not require transparency, and the default material budget remains one dominant Glaze panel plus up to three small floating Glaze controls.

Atmospheric tint and Aura are presentation contributions layered over the material contract. They are never replacements for material opacity, semantic state, or foreground contrast.

## Stability meaning

“Specification-Stable Candidate” means the design decisions are sufficiently bounded and machine-readable for consistent implementation and validation. It does **not** mean Production Stable.

V1.1 can become the official current target only after exact-revision validation, canonical reference scenes, accessibility and performance acceptance, human optical review, platform-native evidence where claimed, synchronized documentation, and a separate governed release/lifecycle promotion.
