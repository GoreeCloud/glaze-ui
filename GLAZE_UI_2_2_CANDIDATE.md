# Glaze UI 2.2 Candidate Contract

**Lifecycle status:** Candidate  
**Candidate line:** 2.2.0-candidate.1  
**Current Stable remains:** 2.1.0  
**Consumer eligible:** No

Glaze UI 2.2 is the next-version GoreeCloud design-system line. The canonical Glaze UI 2.2 design reference defines the target design language, implementation specification, component library, and System Shell / OS Experience. This repository implements that target incrementally and evidence-first.

Nothing in this Candidate contract changes the current Stable consumer target. `VERSION` remains `2.1.0` until the complete 2.2 promotion gate passes on an exact final revision. Candidate behavior must not satisfy Stable consumer conformance.

## 1. Governing design principles

Glaze UI 2.2 carries forward the Stable strengths of 2.1 while sharpening the system around four rules:

- **Content stays clear. Controls become spatial. Motion explains change. Color communicates meaning.**
- **Solid where you read. Glazed where you interact.**
- **Accessibility can simplify every visual effect without reducing capability.**
- **Security interfaces prioritize certainty over beauty.**

The 2.2 identity is a combination of readable neutral surfaces, selective responsive Glaze material, stable semantic color, concentric geometry, adaptive typography and symbols, compact tactile motion, search-centric navigation, contextual capsules, spatial transformation, and first-class accessibility fallbacks. No single visual effect defines conformance.

## 2. Candidate foundation scope

`2.2.0-candidate.1` is a bounded implementation foundation. It currently implements and validates:

1. a machine-readable 2.2 core token contract in `tokens/glaze-2.2.candidate.json`;
2. a machine-readable System Shell contract schema in `schemas/system-shell-contract.schema.json`;
3. a bounded System Shell foundation contract in `contracts/system-shell/glaze-system-shell-2.2.json`;
4. a web Candidate foundation layer in `css/glaze-2.2.candidate.css`;
5. lifecycle separation in `registry/lifecycle.json`;
6. fail-closed structural validation in `scripts/validate_glaze_2_2_candidate.py`;
7. exact-head Candidate CI in `.github/workflows/glaze-2.2-candidate.yml`;
8. a Candidate acceptance boundary in `acceptance/2.2-candidate.md`.

The same Candidate line now also contains separately bounded, fail-closed implementation and evidence tranches for the complete 32-contract component catalog: eight Foundation, eight Structure, six Overlay, five Signature, and five Intelligence contracts. Their web reference layers and rendered acceptance harnesses are validated by the dedicated 2.2 Candidate workflow. Signature includes GlzCapsule, GlzMorphCard, GlzSmartRail, GlzAuroraSurface, and GlzUniversalSearch; Intelligence includes GlzAIAction, GlzAISuggestion, GlzAIAnswer, GlzSmartSummary, and GlzSourceChip.

Additional bounded Candidate evidence includes the Universal Search / Control Center interaction reference in `js/glaze-2.2.system-interactions.candidate.mjs`, the 2.1→2.2 compatibility assessment in `contracts/migration/glaze-2.1-to-2.2.json`, the performance and System Glaze-budget contract in `contracts/performance/glaze-2.2-performance-budget.json`, and the buildable Android-native Candidate reference under `reference/native/android/2.2-candidate/`. These artifacts prove only their recorded scopes; they do not turn the corresponding complete-release lifecycle capabilities into Stable or authorize production consumer migration.

This tranche does **not** claim complete implementation of the Glaze UI 2.2 component catalog across every native platform, complete Universal Search runtime, complete Control Center runtime, window manager, lock/login shell, notification system, system settings, file manager, native platform shell, system intelligence backend, developer packages, generated documentation, or downstream consumer adoption. Those remain separate implementation and evidence workstreams until explicitly implemented and validated.

## 3. Shared interaction state model

The Candidate foundation adopts the 2.2 shared state vocabulary:

`rest → hover → focus → pressed → selected → disabled → loading → error`

When states compete, the semantic priority is:

`disabled > error > pressed > focus > selected > hover > rest`

Components may extend this vocabulary with domain states such as success, warning, offline, protected, restricted, syncing, or indeterminate, but must preserve deterministic precedence and non-color-only meaning.

Interaction state layers are applied over the semantic base surface rather than replacing semantic surface identity. The bounded candidate token ranges are:

- hover: 3–6%
- pressed: 7–12%
- selected: 8–16%

Focus remains explicitly visible and is not subordinated to hover styling.

## 4. Core geometry and target behavior

The Candidate foundation preserves a practical interaction floor of 48 px for touch-oriented shell controls and 56 px when Touch Assistance or far-view requirements apply. Compact pointer-oriented controls may render smaller visual geometry only when the accessible hit target remains appropriate to the input environment.

Primary shell geometry uses a restrained family centered on 12 px, 20 px, 28 px, and pill radii. Large system panels may use 24–32 px geometry. Dense application interiors may remain tighter; the system shell is intentionally softer.

## 5. System Shell surface hierarchy

Glaze UI 2.2 defines five system-level semantic surface classes:

1. **Workspace** — the user's persistent environment;
2. **Application** — windows or full-screen application surfaces;
3. **System Overlay** — search, volume, brightness, media, quick actions, and similar transient controls;
4. **System Panel** — notifications, Control Center, app/window switching, and system panels;
5. **Critical System** — authentication, security warnings, shutdown, recovery, and similarly high-stakes surfaces.

Higher-priority system layers become progressively more solid and explicit. Security-critical interaction must never depend on decorative transparency over complex content.

The shell hierarchy is:

**Workspace → Apps → Context → System**

The system should remain quiet until requested and immediately available when summoned.

## 6. System Glaze budget

The Candidate foundation encodes the 2.2 shell restraint rule: under ordinary conditions, a shell should show no more than **one dominant Glaze panel plus one to three small floating Glaze controls** at once unless the interaction explicitly requires more.

Nested backdrop blur is prohibited as a design strategy. The conceptual render stack is:

`content → single environmental diffusion → foreground material`

Dense reading or configuration content remains primarily solid. Glaze is an interaction-depth tool, not wallpaper.

## 7. System motion hierarchy

The Candidate token contract defines bounded system timing ranges:

- popover: 160–200 ms;
- Control Center: 220–280 ms;
- Universal Search: 240–320 ms;
- workspace transitions: 320–420 ms;
- unlock transitions: 280–420 ms.

The semantic motion hierarchy is:

- small state → Snap;
- panel → Glide;
- workspace → Spatial Glide;
- direct manipulation → Spring.

Keyboard traversal, direct manipulation, focus movement, and semantic state changes must not wait for decorative animation to finish.

## 8. Accessibility resolution

Every system feature must retain an alternative path that does not depend on precision gestures, color, transparency, animation, sound, or hover.

The Candidate web layer includes explicit Reduced Motion, Reduced Transparency, Increased Contrast, and Forced Colors fallbacks. Reduced Motion replaces large spatial movement and decorative morphing with short crossfades, opacity changes, or small-scale feedback while preserving direct manipulation. Reduced Transparency replaces Glaze materials with increasingly opaque surfaces while preserving hierarchy through border, elevation, and tonal separation.

High Contrast strengthens focus, boundaries, selected indicators, panel opacity, and status clarity. Semantic meaning remains available through text, icons, shape, and programmatic semantics rather than color alone.

## 9. Deep Dark foundation

The Candidate foundation encodes the documented Deep Dark shell anchors:

- Canvas: `#05070A`
- Base: `#0D1015`
- Raised: `#171C23`

Routine UI highlights must not consume maximum HDR luminance. Glaze surfaces remain distinguishable from the Canvas without turning large regions into high-luminance panels.

## 10. System typography and symbols

Initial shell token ranges are:

- shell labels: 13–15 px;
- panel titles: 18–22 px;
- workspace titles: 22–28 px;
- lock-screen time: 56–88 px;
- common system symbols: 20–24 px.

System UI must not depend on ultra-thin typography. Critical status symbols may use stronger optical weight, but critical meaning also requires an explicit semantic label or notification where appropriate.

## 11. System color and privacy boundaries

Color remains secondary to labels and symbols. The initial category identities are encoded as bounded Candidate metadata, not permission for decorative saturation. Semantic warning, critical, danger, security, success, privacy, and accessibility meaning overrides application or wallpaper color.

Wallpaper may influence ambient shell tint only within a clamped range. It must never alter semantic meanings.

Privacy state must be visible, understandable, and actionable. Sensor or recording status is a system-level truth surface and must not be hidden by application styling.

## 12. Candidate web implementation

`css/glaze-2.2.candidate.css` is the shell foundation reference layer. The Candidate implementation also includes the separately bounded component layers `css/glaze-2.2.components.candidate.css`, `css/glaze-2.2.components.adaptive.candidate.css`, `css/glaze-2.2.components.runtime.candidate.css`, `css/glaze-2.2.structure.candidate.css`, `css/glaze-2.2.overlay.candidate.css`, and `css/glaze-2.2.advanced.candidate.css`.

Together, the bounded reference layers provide:

- core 2.2 semantic custom properties;
- Workspace, Application, System Overlay, System Panel, Critical System, Capsule, and system-status roles;
- bounded Foundation, Structure, Overlay, Signature, and Intelligence component presentation;
- bounded Glaze material and shadow behavior;
- visible keyboard focus;
- Reduced Motion and Reduced Transparency fallbacks;
- Increased Contrast and Forced Colors fallbacks;
- Deep Dark anchors;
- shell target-size and typography primitives.

These web layers are evidence for their bounded reference scopes only. They are not an operating system, compositor, window manager, notification daemon, search index, authentication provider, privacy authority, intelligence backend, or native-platform certification.

## 13. Candidate implementation discipline

2.2 implementation work must remain staged. A capability becomes Candidate only when a concrete repository artifact and objective validation exist. Planned specifications stay Planned until that boundary is crossed. Bounded implementation evidence must not be generalized into a complete-release claim when the lifecycle registry still records the broader capability as Planned.

The lifecycle registry is authoritative for release and capability state. Documentation, tokens, code, acceptance records, and CI must not disagree about the current Stable version or Candidate line.

Glaze Motion remains separately governed and Experimental unless explicitly promoted through its own evidence path. 2.2 may map to its semantics without silently promoting it.

## 14. Stable promotion gate

Glaze UI 2.2 may become Stable only after the applicable current governance gates are complete on exact final revisions, including:

- complete release contract and migration boundary;
- machine-readable token/component/material/system-shell contracts for the promoted scope;
- executable reference implementation where applicable;
- exact-revision repository CI;
- rendered acceptance across representative form factors and appearances;
- accessibility and resilience acceptance, including Reduced Motion, Reduced Transparency, Increased Contrast, Forced Colors, large text, keyboard, touch, and pointer paths as applicable;
- regression evidence for state, interaction, responsive transformation, and visual output;
- native or device evidence for any design-system-native behavior claimed by the release;
- performance and Glaze-budget validation;
- compatibility and migration analysis from 2.1.0;
- recorded human Visual Excellence review for the final presentation;
- lifecycle, version, changelog, acceptance, rollback, and release records aligned to the exact final revision.

If any applicable gate is incomplete, Glaze UI 2.2 remains Candidate.

## 15. Consumer boundary

No downstream GoreeCloud application is promoted by declaration. While 2.2 remains Candidate, all production consumers continue targeting Glaze UI 2.1.0 Stable. After a future 2.2 Stable promotion, each consumer will still require its own exact-revision adoption and acceptance before it may claim current 2.2 conformance.

The Candidate rule is therefore explicit:

> **2.2 is being built in public evidence. It is not Stable until the evidence says it is Stable.**
