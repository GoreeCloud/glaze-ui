# Glaze UI 2.2 Candidate Contract

**Lifecycle status:** Candidate  
**Candidate line:** 2.2.0-candidate.1  
**Current Stable remains:** 2.1.0  
**Consumer eligible:** No

Glaze UI 2.2 is the next-version GoreeCloud design-system line. The canonical Glaze UI 2.2 design reference defines the target design language, implementation specification, component library, and System Shell / OS Experience. This repository implements that target incrementally and evidence-first.

Nothing in this Candidate contract changes the current Stable consumer target. `VERSION` remains `2.1.0` until the complete 2.2 promotion gate passes on an exact final revision. Candidate behavior must not satisfy Stable consumer conformance.

## 1. Governing design principles

Glaze UI 2.2 carries forward the Stable strengths of 2.1 while sharpening the system around these rules:

- **Content stays clear. Controls become spatial. Motion explains change. Color communicates meaning.**
- **Solid where you read. Glazed where you interact.**
- **Accessibility can simplify every visual effect without reducing capability.**
- **Security interfaces prioritize certainty over beauty.**
- **Reachability and optical depth must reinforce each other rather than compete.**

The active Candidate visual refinement is named **Optical Reachability**. It is an original GoreeCloud synthesis of spacious, thumb-friendly, modular interaction geometry with selective translucent depth, optical edges, highlights, and floating system chrome. It is not a clone of another platform and must preserve GoreeCloud semantic, accessibility, privacy, and performance rules.

Optical Reachability uses larger sculpted controls, contained selection capsules, context-aware floating navigation/search surfaces, restrained environmental depth, and increasingly solid high-priority surfaces. Optical treatment is never required to understand state or meaning.

## 2. Candidate foundation scope

`2.2.0-candidate.1` is a bounded implementation foundation. It includes machine-readable 2.2 tokens, System Shell contracts, lifecycle separation, exact-head CI, a complete 32-contract component catalog, bounded web reference layers, Universal Search / Control Center interaction references, migration compatibility assessment, performance / System Glaze-budget evidence, an Android-native Candidate reference, and reproducible rendered/review evidence.

The 32-contract catalog is:

- Foundation: 8 — GlzButton, GlzIconButton, GlzTextField, GlzSelect, GlzCheckbox, GlzRadio, GlzSwitch, GlzSlider;
- Structure: 8 — GlzCard, GlzList, GlzTable, GlzTabs, GlzSidebar, GlzNavigationRail, GlzDock, GlzToolbar;
- Overlay: 6 — GlzTooltip, GlzPopover, GlzMenu, GlzDialog, GlzSheet, GlzToast;
- Signature: 5 — GlzCapsule, GlzMorphCard, GlzSmartRail, GlzAuroraSurface, GlzUniversalSearch;
- Intelligence: 5 — GlzAIAction, GlzAISuggestion, GlzAIAnswer, GlzSmartSummary, GlzSourceChip.

The bounded Optical Reachability tranche adds:

- `css/glaze-2.2.visual-refinement.candidate.css` — System Shell / review-surface visual refinement;
- `css/glaze-2.2.optical-reachability.candidate.css` — consolidated component presentation refinement;
- `reference/candidate-2.2-optical-reachability-acceptance.html` — component-system presentation acceptance surface;
- `scripts/validate_glaze_2_2_optical_reachability.py` — static/lifecycle fail-closed gate;
- `scripts/validate_glaze_2_2_optical_reachability_rendered.py` — 15-case rendered presentation matrix;
- `scripts/capture_glaze_2_2_optical_component_review.py` — exact-head six-image component review capture.

These artifacts prove only their recorded scopes. They do not turn broader complete-release capabilities into Stable or authorize production consumer migration.

This Candidate does **not** claim complete product adoption across every GoreeCloud application, complete cross-platform native implementation, operating-system services, production Universal Search indexing, production Control Center integration, authentication/privacy/intelligence backends, downstream consumer migration, or Human Visual Excellence approval.

## 3. Shared interaction state model

The Candidate foundation adopts the 2.2 shared state vocabulary:

`rest → hover → focus → pressed → selected → disabled → loading → error`

When states compete, semantic priority is:

`disabled > error > pressed > focus > selected > hover > rest`

Components may extend this vocabulary with domain states such as success, warning, offline, protected, restricted, syncing, or indeterminate, but must preserve deterministic precedence and non-color-only meaning.

Interaction state layers are applied over the semantic base surface rather than replacing semantic identity. Focus remains explicitly visible and is not subordinated to hover or selected styling.

## 4. Core geometry and target behavior

The Candidate preserves a practical interaction floor of 48 px for touch-oriented shell controls and 56 px when Touch Assistance or far-view requirements apply. Compact pointer-oriented visual geometry may be smaller only where the input environment and accessible hit target remain appropriate.

Optical Reachability refines the geometry family toward sculpted 16–24 px controls, 24–30 px content/chrome containers, and pills/capsules where the interaction is conceptually continuous. Dense application interiors may remain tighter. Large text must reflow rather than shrink targets or clip content.

## 5. System Shell surface hierarchy

Glaze UI 2.2 defines five system-level semantic surface classes:

1. **Workspace** — the user's persistent environment;
2. **Application** — windows or full-screen application surfaces;
3. **System Overlay** — search, volume, brightness, media, quick actions, and similar transient controls;
4. **System Panel** — notifications, Control Center, app/window switching, and system panels;
5. **Critical System** — authentication, security warnings, shutdown, recovery, and similarly high-stakes surfaces.

Higher-priority system layers become progressively more solid and explicit. The shell hierarchy is:

**Workspace → Apps → Context → System**

Critical System interaction must never depend on decorative transparency over complex content.

## 6. System Glaze budget

Under ordinary conditions, a shell should show no more than **one dominant Glaze panel plus one to three small floating Glaze controls** at once unless the interaction explicitly requires more.

Nested backdrop blur is prohibited as a design strategy. The conceptual render stack remains:

`content → single environmental diffusion → foreground material`

Optical Reachability does not expand the Glaze budget. It changes geometry, layering, edge treatment, and reachability within the existing performance restraint.

## 7. System motion hierarchy

The Candidate token contract defines bounded system timing ranges:

- popover: 160–200 ms;
- Control Center: 220–280 ms;
- Universal Search: 240–320 ms;
- workspace transitions: 320–420 ms;
- unlock transitions: 280–420 ms.

The semantic hierarchy is small state → Snap, panel → Glide, workspace → Spatial Glide, direct manipulation → Spring. Keyboard traversal, direct manipulation, focus movement, and semantic state changes must not wait for decorative animation.

## 8. Accessibility resolution

Every system feature must retain an alternative path that does not depend on precision gestures, color, transparency, animation, sound, or hover.

Reduced Motion removes or simplifies large spatial movement. Reduced Transparency replaces Optical Glaze with increasingly opaque surfaces while preserving hierarchy through boundaries, elevation, and tonal separation. Increased Contrast strengthens focus, boundaries, selected indicators, and status clarity. Forced Colors removes decorative Glaze and preserves system colors and focus semantics.

The active Optical Reachability rendered matrix explicitly covers mobile touch, tablet, desktop, wide desktop, Dark, Deep Dark, Reduced Motion, Reduced Transparency, Increased Contrast, Forced Colors, RTL, 200% text, and Touch Assistance states.

## 9. Deep Dark foundation

The Candidate retains the documented Deep Dark shell anchors:

- Canvas: `#05070A`
- Base: `#0D1015`
- Raised: `#171C23`

Routine UI highlights must not consume maximum HDR luminance. Optical surfaces remain distinguishable from Canvas without turning large regions into high-luminance panels.

## 10. System typography and symbols

Initial shell token ranges remain:

- shell labels: 13–15 px;
- panel titles: 18–22 px;
- workspace titles: 22–28 px;
- lock-screen time: 56–88 px;
- common system symbols: 20–24 px.

System UI must not depend on ultra-thin typography. Critical meaning requires explicit semantics in addition to visual emphasis.

## 11. System color and privacy boundaries

Color remains secondary to labels and symbols. Semantic warning, critical, danger, security, success, privacy, and accessibility meaning overrides decorative application/wallpaper color.

Wallpaper may influence ambient shell tint only within a clamped range. Privacy state must remain visible, understandable, and actionable. Sensor or recording status is a system truth surface and must not be hidden by product styling.

## 12. Candidate web implementation

`css/glaze-2.2.candidate.css` remains the shell foundation reference layer. Bounded component layers include:

- `css/glaze-2.2.components.candidate.css`;
- `css/glaze-2.2.components.adaptive.candidate.css`;
- `css/glaze-2.2.components.runtime.candidate.css`;
- `css/glaze-2.2.structure.candidate.css`;
- `css/glaze-2.2.overlay.candidate.css`;
- `css/glaze-2.2.advanced.candidate.css`;
- `css/glaze-2.2.visual-refinement.candidate.css`;
- `css/glaze-2.2.optical-reachability.candidate.css`.

The tier layers remain separately bounded rather than being silently collapsed into a release package. Optical Reachability is a presentation refinement composed with the appropriate tier base in its acceptance surface. This avoids inventing a Stable consumer entrypoint while 2.2 remains Candidate.

Together, the bounded reference layers provide core semantic custom properties, System Shell roles, complete contract-tier presentation, selective Glaze material, visible focus, accessibility fallbacks, Deep Dark, target-size primitives, and the active Optical Reachability geometry/depth language.

## 13. Candidate implementation discipline

2.2 implementation remains evidence-first. A capability becomes Candidate only when concrete repository artifacts and objective validation exist. Planned specifications stay Planned until that boundary is crossed. Bounded evidence must not be generalized into complete-release claims.

The lifecycle registry records Optical Reachability, Android emulator acceptance, component contracts, system interactions, migration, performance, and visual evidence separately from broader product/runtime/full-release capabilities.

The pre-Optical-Reachability source-pinned screenshot baseline remains historical Candidate evidence for the presentation it covered. It is explicitly non-current for the active redesign. A replacement baseline must not be created merely to turn CI green.

## 14. Stable promotion gate

Glaze UI 2.2 may become Stable only after applicable governance gates are complete on exact final revisions, including:

- complete release contract and migration boundary;
- machine-readable token/component/material/System Shell contracts for the promoted scope;
- executable reference implementation where applicable;
- exact-revision repository CI;
- rendered acceptance across representative form factors and appearances;
- accessibility and resilience acceptance including Reduced Motion, Reduced Transparency, Increased Contrast, Forced Colors, large text, keyboard, touch, and pointer paths;
- interaction and visual regression evidence;
- native/device evidence for claimed design-system-native behavior;
- performance and Glaze-budget validation;
- compatibility and migration analysis from 2.1.0;
- **recorded human Visual Excellence review for the active final presentation**;
- a human-approved immutable visual baseline for that presentation;
- lifecycle, version, changelog, acceptance, rollback, and release records aligned to the exact final revision.

For Optical Reachability, automated presentation/rendered/review capture evidence is now bounded Candidate evidence, but Human Visual Excellence remains Pending. Until that review occurs, the active redesign intentionally remains blocked by the historical pre-redesign pixel baseline.

If any applicable gate is incomplete, Glaze UI 2.2 remains Candidate.

## 15. Consumer boundary

No downstream GoreeCloud application is promoted by declaration. While 2.2 remains Candidate, production consumers continue targeting Glaze UI 2.1.0 Stable. After any future 2.2 Stable promotion, each consumer still requires its own exact-revision adoption and acceptance before claiming 2.2 conformance.

The Candidate rule remains explicit:

> **2.2 is being built in public evidence. It is not Stable until the evidence says it is Stable.**
