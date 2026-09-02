# Migrating from Glaze UI 2.1 to 2.2

Status: **Stable migration contract**  
Source Stable: **2.1.0**  
Current Stable target: **2.2.0**  
Promoted from: **2.2.0-candidate.1**  
Production migration authorized: **Yes, through repository-local evidence gates**  
Automatic downstream production eligibility: **No**

This document defines the compatibility boundary and controlled migration path from Glaze UI 2.1.0 to Glaze UI 2.2.0 Stable. Central design-system promotion authorizes consumers to begin a production migration to the Stable target; it does not auto-migrate or auto-approve any downstream GoreeCloud application.

## Compatibility position

Glaze UI 2.2.0 is an additive semantic refinement of the Glaze UI 2.x identity, not a drop-in declaration change. The core rules that made 2.1 reliable remain valid: content stays readable on solid surfaces, transient interaction may use bounded Glaze material, semantic meaning does not depend on color alone, accessibility preferences can remove decorative effects without removing capability, target floors remain input-appropriate, and downstream applications require their own adoption evidence.

2.2 adds a more explicit System Shell hierarchy, a complete 32-component Stable catalog, Signature and Intelligence tiers, stronger spatial interaction semantics, bounded Universal Search and Control Center runtime behavior, a stricter one-dominant-panel System Glaze budget, explicit generated-content provenance, and more precise responsive/accessibility acceptance. Those additions can expose assumptions in a 2.1 consumer that must be remapped deliberately.

The migration position is therefore:

- **2.2.0 is the required current Stable design-system target.**
- **2.1.0 is retained as the historical rollback baseline.**
- **No production consumer may use `2.2.0-candidate.1` or Candidate-named files as production aliases.**
- **A 2.2.0 adoption is repository-local and evidence-based; it is never inferred from central release promotion.**
- **Successful 2.1 task structure and product personality should be preserved rather than visually rewritten for novelty.**

## Preserved compatibility guarantees

The following 2.1 expectations carry forward into 2.2 and should not require product-level redesign when already implemented correctly:

- content-first composition and the rule **Solid where you read. Glazed where you interact.**;
- Light, Dark, and Deep Dark support;
- explicit Reduced Motion, Reduced Transparency, Increased Contrast, Forced Colors, 200% text, keyboard, touch, and pointer paths;
- a 48 px/dp effective touch-oriented target floor and a 56 px/dp Touch Assistance / far-view floor;
- visible focus that remains stronger than hover decoration;
- semantic state that remains understandable without color alone;
- native/platform authority for forced colors, security, privacy, and device state;
- performance fallbacks that simplify effects before semantics or target geometry;
- consumer-specific acceptance and Human Visual Excellence review after design-system adoption; and
- the rule that Experimental Glaze Motion behavior is not silently promoted by Glaze UI.

## 2.2 changes every consumer must evaluate

### Component contracts

Glaze UI 2.2 defines a 32-component Stable catalog across five tiers:

- Foundation: 8 components;
- Structure: 8 components;
- Overlay: 6 components;
- Signature: 5 components; and
- Intelligence: 5 components.

A migrating consumer must map each locally consumed control or composite to the 2.2 semantic contract it actually satisfies. Similar appearance is not sufficient. Focus, state priority, target geometry, API semantics, localization, RTL, fallback behavior, and error association must remain correct.

### System Shell hierarchy

2.2 formalizes five system-level surfaces:

`Workspace → Application → System Overlay → System Panel → Critical System`

Application content remains solid by default. Transient interaction may use Glaze. System Panel content becomes denser and more explicit than System Overlay content, and Critical System is intentionally solid and certainty-first.

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
- explicit source provenance for generated answers when available;
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

## Stable implementation boundary

The current Stable web entrypoint is `css/glaze-2.2.0.css` and the current Stable runtime entrypoint is `js/glaze-2.2.0.mjs`. These Stable entrypoints preserve the reviewed 2.2 Candidate implementation as promotion provenance.

Candidate filenames such as `*.candidate.css` and `*.candidate.mjs` remain release-review provenance. They are not permanent production compatibility aliases and must not be imported directly by a production consumer claiming current-Stable conformance.

## Consumer migration sequence

1. Record the exact Glaze UI 2.2.0 Stable release revision and immutable release/tag anchor.
2. Create a repository-local adoption change; do not infer adoption from the central lifecycle registry.
3. Inventory the application’s consumed components, overlays, navigation, search, intelligent/generated surfaces, density profiles, materials, and platform-state UI.
4. Map each consumed element to the 2.2 semantic component or system-surface contract.
5. Replace direct Candidate implementation imports with the 2.2.0 Stable entrypoints where applicable.
6. Resolve any multi-panel Glaze composition against the 2.2 System Glaze budget rather than adding exceptions by default.
7. Re-run keyboard, pointer, touch, 200% text, RTL/localization, Reduced Motion, Reduced Transparency, Increased Contrast, Forced Colors, Touch Assistance, and applicable native/platform acceptance.
8. Validate application-specific performance and effect fallbacks on representative supported hardware.
9. Validate generated/AI content provenance and dismissal behavior anywhere Intelligence components are adopted.
10. Perform application-specific Human Visual Excellence review on the exact adoption revision.
11. Update repository-local conformance evidence and the canonical GoreeCloud consumer registry only from verified application evidence.
12. Keep application production eligibility false until its own 2.2 adoption gates pass.

## Compatibility classification

For the design-system release itself, 2.1 → 2.2 is classified as an **additive semantic refinement with explicit adoption work**. This classification does not promise compatibility for Candidate implementation filenames.

The following remain conceptually compatible:

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
- 2.2 Stable package/entrypoint names.

## Rollback

Glaze UI 2.1.0 is the historical rollback reference for the 2.2.0 release. A temporary rollback may support diagnosis or recovery, but it does not make a downstream consumer conformant with the current Stable design-system target.

Consumers must preserve exact prior adoption revisions, migration notes, and acceptance evidence so regressions can be diagnosed without force-pushing or rewriting history.

## Non-claims

This migration contract does not establish that:

- every 2.1 application is automatically 2.2-compatible;
- any downstream application is production eligible merely because 2.2.0 is Stable;
- Candidate web/runtime filenames are permanent Stable API names;
- design-system native reference evidence certifies downstream native applications; or
- design-system Human Visual Excellence approval substitutes for application-specific visual review.

## Promotion and adoption boundary

The design-system migration gate is satisfied only when this machine-readable contract and its fail-closed validator pass on the exact 2.2 Stable promotion revision and remain aligned with the implemented 2.2 scope. Downstream adoption remains separately gated by repository-local implementation, automated validation, rendered/native/accessibility evidence, Human Visual Excellence where applicable, release approval, and production acceptance.
