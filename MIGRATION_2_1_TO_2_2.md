# Migrating from Glaze UI 2.1 to 2.2

Status: **Candidate migration assessment**  
Current Stable: **2.1.0**  
Target under review: **2.2.0-candidate.1**  
Production migration authorized: **No**

This document defines the compatibility boundary and controlled migration path from Glaze UI 2.1.0 Stable to the active Glaze UI 2.2 Candidate. It is release evidence, not permission for a downstream GoreeCloud application to adopt a Candidate as its production design-system target.

## Compatibility position

Glaze UI 2.2 is a compatible refinement of the Glaze UI 2.x identity, but it is not a drop-in declaration change. The core rules that made 2.1 Stable remain valid: content stays readable on solid surfaces, interaction may use bounded Glaze material, semantic meaning does not depend on color alone, accessibility preferences can remove decorative effects without removing capability, target floors remain input-appropriate, and downstream applications require their own adoption evidence.

2.2 adds a more explicit System Shell hierarchy, a complete 32-component contract catalog, Signature and Intelligence tiers, stronger spatial interaction semantics, Universal Search and Control Center runtime behavior, a stricter one-dominant-panel System Glaze budget, explicit AI/generated-content provenance, and more precise responsive/accessibility acceptance. Those additions can expose assumptions in a 2.1 consumer that must be remapped deliberately.

The migration position is therefore:

- **2.1.0 remains the rollback and production baseline until 2.2 is formally Stable.**
- **No production consumer may switch to `2.2.0-candidate.1`.**
- **A future 2.2 Stable adoption is repository-local and evidence-based; it is never inferred from central release promotion.**
- **Successful 2.1 task structure and product personality should be preserved rather than visually rewritten for novelty.**

## Preserved compatibility guarantees

The following 2.1 expectations carry forward into 2.2 and should not require product-level redesign when already implemented correctly:

- content-first composition and the rule **Solid where you read. Glazed where you interact.**;
- Light, Dark, and Deep Dark support;
- explicit Reduced Motion, Reduced Transparency, Increased Contrast, Forced Colors, large-text, keyboard, touch, and pointer paths;
- a 48 px/dp effective touch-oriented target floor and a 56 px/dp Touch Assistance / far-view floor;
- visible focus that remains stronger than hover decoration;
- semantic state that remains understandable without color alone;
- native/platform authority for forced colors, security, privacy, and device state;
- performance fallbacks that simplify effects before semantics or target geometry;
- consumer-specific acceptance and Human Visual Excellence review after design-system adoption; and
- the rule that experimental Glaze Motion behavior is not silently promoted by Glaze UI.

## 2.2 changes every consumer must evaluate

### Component contracts

Glaze UI 2.2 defines a 32-component Candidate catalog across five tiers:

- Foundation: 8 components;
- Structure: 8 components;
- Overlay: 6 components;
- Signature: 5 components; and
- Intelligence: 5 components.

A migrating consumer must map each locally consumed control or composite to the 2.2 semantic contract it actually satisfies. Similar appearance is not sufficient. Focus, state priority, target geometry, API semantics, localization, RTL, fallback behavior, and error association must remain correct.

### System Shell hierarchy

2.2 formalizes five system-level surfaces:

`Workspace → Application → System Overlay → System Panel → Critical System`

Application content remains solid by default. Transient interaction may use Glaze. System Panel content becomes denser/more explicit than System Overlay content, and Critical System is intentionally solid and certainty-first.

A 2.1 consumer must not map every floating surface to the same material merely because it previously used a Glaze-like appearance.

### System Glaze budget

Ordinary 2.2 shell composition permits at most one dominant Glaze panel plus one to three small floating Glaze controls. More requires an explicit exceptional context. Nested backdrop blur is not a valid composition strategy.

Consumers that currently stack multiple simultaneous translucent drawers, palettes, or sheets must resolve the semantic ownership of those surfaces during migration rather than disabling the budget validator.

### State and interaction

2.2 uses the shared state vocabulary:

`rest → hover → focus → pressed → selected → disabled → loading → error`

and semantic priority:

`disabled > error > pressed > focus > selected > hover > rest`

Domain states may extend this set, but competing state presentation must remain deterministic. Keyboard traversal, direct manipulation, focus movement, and semantic state changes never wait for decorative animation.

### Universal Search

Universal Search is a central 2.2 system interaction rather than a decorative search field. Migration must preserve:

- immediate query focus when invoked;
- deterministic source/results ordering before generated interpretation;
- keyboard result traversal;
- explicit source provenance for generated answers;
- a second explicit activation before destructive search actions execute;
- Escape canceling an active destructive confirmation before closing the search surface; and
- meaningful focus restoration on close.

Applications may keep local search when appropriate; they should not relabel local search as Universal Search unless it satisfies the system-level contract.

### Control Center

Control Center uses semantic system controls rather than simulated cards. Toggle state must be programmatically available, range controls must expose real values, and the panel must not stack with Universal Search as a second dominant Glaze surface. Closing the panel restores a meaningful invoker focus.

### Signature components

Capsule, Morph Card, Smart Rail, Aurora Surface, and Universal Search introduce spatial continuity rules that should be adopted only where they explain a real relationship. Migration must not replace conventional controls with Signature components merely to appear more “2.2”. Reduced Motion must retain the same destination, focus, and capability without requiring spatial travel.

### Intelligence components

AI Action, AI Suggestion, AI Answer, Smart Summary, and Source Chip require explicit generated/AI identity, source provenance when available, calibrated language, nonblocking behavior, and dismissibility where appropriate. Generated interpretation must remain distinct from retrieved source content.

A consumer must not use Aurora color, spark icons, or labels as a substitute for provenance or uncertainty semantics.

## Web implementation boundary

The current 2.1 Stable web entrypoint remains `css/glaze-2.1.0.css`. The 2.2 Candidate implementation is intentionally separate and must not be imported into a production consumer as if it were the current Stable entrypoint.

A future Stable migration should change the design-system target only after the final 2.2 Stable artifact exists. Candidate filenames such as `*.candidate.css` and `*.candidate.mjs` are release-review artifacts, not production compatibility aliases.

## Consumer migration sequence

1. Keep the application on Glaze UI 2.1.0 while 2.2 remains Candidate.
2. When 2.2 is formally promoted, record the exact 2.2 Stable release revision and release artifact.
3. Create a repository-local adoption change; do not infer adoption from the central lifecycle registry.
4. Inventory the application’s consumed components, overlays, navigation, search, intelligent/generated surfaces, density profiles, materials, and platform-state UI.
5. Map each consumed element to the 2.2 semantic component or system-surface contract.
6. Resolve any multi-panel Glaze composition against the 2.2 System Glaze budget rather than adding exceptions by default.
7. Re-run keyboard, pointer, touch, large-text, RTL/localization, Reduced Motion, Reduced Transparency, Increased Contrast, Forced Colors, Touch Assistance, and applicable native/platform acceptance.
8. Validate application-specific performance and effect fallbacks on representative supported hardware.
9. Validate generated/AI content provenance and dismissal behavior anywhere Intelligence components are adopted.
10. Perform application-specific Human Visual Excellence review on the exact adoption revision.
11. Update repository-local conformance evidence and the canonical GoreeCloud consumer registry only from verified application evidence.
12. Keep application production eligibility false until its own 2.2 adoption gates pass.

## Compatibility classification

For the design-system release itself, 2.1 → 2.2 is classified as an **additive semantic refinement with explicit adoption work**, not an automatic API compatibility promise for Candidate implementation filenames.

The following are expected to remain conceptually compatible:

- core visual identity;
- content/material hierarchy;
- accessibility authority and fallback philosophy;
- state semantics;
- target-size floors;
- density intent;
- semantic-color authority; and
- downstream evidence requirements.

The following require explicit migration review:

- 2.2 component contract/API mappings;
- System Shell surface classification;
- Signature spatial transformation behavior;
- Universal Search integration;
- Control Center integration;
- System Glaze budget compliance;
- Intelligence/generated-content provenance;
- 2.2 native reference behavior; and
- any future 2.2 Stable package/entrypoint names.

## Rollback

Until 2.2 is Stable, rollback is simply **remain on Glaze UI 2.1.0 Stable**. Candidate experiments must be isolated so they can be removed without rewriting the 2.1 production history.

After a future 2.2 Stable promotion, 2.1.0 becomes a historical rollback reference. A temporary rollback may support diagnosis or recovery, but it does not make an outdated consumer conformant with the current Stable design-system target.

Consumers must preserve exact prior adoption revisions, migration notes, and acceptance evidence so regressions can be diagnosed without force-pushing or rewriting history.

## Non-claims

This migration assessment does not establish that:

- Glaze UI 2.2 is Stable;
- `2.2.0-candidate.1` is production consumer eligible;
- every 2.1 application is automatically 2.2-compatible;
- Candidate web/runtime filenames are permanent Stable API names;
- design-system native reference evidence certifies downstream native applications; or
- design-system Human Visual Excellence approval substitutes for application-specific visual review.

## Promotion boundary

This document satisfies the migration-analysis documentation gate only when its machine-readable companion and fail-closed validator pass on the exact Candidate revision and remain aligned with the implemented 2.2 scope. Stable promotion still requires all other applicable gates, including full rendered/interaction and visual regression, native/device evidence where claimed, performance and Glaze-budget acceptance, release records, and recorded human Visual Excellence approval.
