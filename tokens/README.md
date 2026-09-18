# GLAZE UI Token Authority

`VERSION` and `registry/lifecycle.json` are the current lifecycle identity authorities. The current Official Stable release is **GLAZE UI V1.5 / `1.5.1`**.

The token directory intentionally preserves source files from earlier Stable and Candidate qualification lines. Historical `.candidate` suffixes and older product/version fields are retained where they are part of immutable source provenance; they do not override current lifecycle authority.

## Current and historical token roles

`tokens/glaze-v1.json` is the retained V1.2-era Stable token manifest used for historical verification and provenance. It must not be interpreted as the current repository lifecycle version merely because it remains present.

Existing token families continue to provide value authority for color, typography, spacing, geometry, shape, material, depth, motion, iconography, interaction states, layout, and form-factor semantics inherited by later Glaze releases.

## Experience Language Development ownership map

`tokens/glaze-experience-language.dev.json` is a **Development, reference-only, non-consumer-eligible ownership map** for the broader Glaze UI Visual, Spatial, and Interaction Language. It defines the required token categories:

- color
- typography
- spacing
- radius
- border
- shadow
- elevation
- opacity
- blur
- motion
- size
- icon
- breakpoint

The map points each semantic category to existing repository token sources instead of copying raw values or manufacturing a competing authority. It also identifies composition sources for interaction states, spatial behavior, materials, icons, and motion.

This Development map does not modify Stable token values, `VERSION`, lifecycle state, release evidence, or downstream consumer acceptance. Future promotion requires the applicable governed release and exact-revision qualification process.

Token presence, alias resolution, or Development source validation alone never establishes downstream conformance, target-runtime acceptance, deployment, or production eligibility.


## V1.6 loading and skeleton Development semantic map

`tokens/glaze-v1.6-loading.dev.json` is the first V1.6-specific **Development, non-consumer-eligible semantic map**. It covers skeleton surfaces, geometry, motion modes, loading state, progress, recovery presentation, accessibility fallbacks, performance levels, and motion-fatigue protection.

The map inherits Stable V1.5.1 authorities from `tokens/motion.json`, `tokens/states.json`, `tokens/layout.json`, and `tokens/materials.json` rather than replacing their current Stable values. It adds V1.6 semantic intent for the Development loading/skeleton resolver while preserving these boundaries:

- Reduced Motion maps continuous skeleton motion to `static`.
- Reduced Transparency maps skeleton presentation to solid surfaces.
- Increased Contrast and Forced Colors prohibit opacity-only differentiation.
- Determinate progress requires truthful progress values; fake percentages are forbidden.
- Efficient and Essential performance levels disable continuous skeleton motion.
- Many simultaneous skeletons trigger motion-fatigue protection rather than multiplying shimmer.

This map is Development source only. It does not change `VERSION`, lifecycle state, current Stable token authority, consumer eligibility, downstream conformance, deployment, or production status.


## V1.6 state, accessibility, and performance Development semantic map

`tokens/glaze-v1.6-state-accessibility.dev.json` is a **Development, non-consumer-eligible semantic map** for the implemented V1.6 state/accessibility/performance foundation.

It aliases existing current/historical token authorities rather than replacing Stable V1.5.1 values and establishes Development semantics for:

- the 26-state V1.6 semantic state grammar;
- protected semantic foreground/background roles;
- non-color state differentiation;
- capability-state distinctions for Disabled, Unavailable, Restricted, Unsupported, Permission required, Temporarily unavailable, and Unknown;
- the 13 accessibility profiles and the token domains each profile may constrain;
- Full, Balanced, Efficient, and Essential visual-performance levels;
- anti-jitter stability windows, dwell, coalescing, and hysteresis behavior.

Accessibility profiles resolve only from supplied authoritative preferences. The state map does not infer privacy, security, authorization, or provider precedence. Performance adaptation may reduce visual cost but may not rewrite capability truth or interaction authority.

This map does not change `VERSION`, `registry/lifecycle.json`, Stable token values, consumer eligibility, downstream acceptance, release publication, deployment, or production state.


## V1.6 focus and motion Development semantic map

`tokens/glaze-v1.6-focus-motion.dev.json` is a **Development, non-consumer-eligible semantic map** for the unified V1.6 focus, motion, microinteraction, and continuity foundation.

It defines semantic aliases and bounded presentation roles for:

- material-aware visible focus that remains distinct from selection, hover, press, activation, and drag;
- 17 semantic motion families covering enter/exit, expansion/collapse, movement/reorder, replacement/reveal/hide, focus/select, loading/refresh, completion/failure, and connection/disconnection;
- motion magnitude tied to decoration, secondary, primary, and navigation hierarchy;
- reference fatigue budgets for continuous animation, simultaneous transitions, background material movement, skeleton motion, decorative movement, and large-area transformations;
- Reduced Motion fallbacks that preserve state and direct manipulation without requiring spatial travel;
- 14 reusable microinteraction intents;
- same-identity state continuity and focus/scroll-preserving content replacement.

The map consumes existing Stable motion/state/material/layout authorities and the V1.6 accessibility foundation. It does not promote Glaze Motion: that system remains separately governed as an Experimental foundation.

This map does not change `VERSION`, lifecycle authority, Stable token values, consumer eligibility, downstream acceptance, release publication, deployment, or production state.


## V1.6 material, typography, density, and input Development semantic map

`tokens/glaze-v1.6-material-type-input.dev.json` is a **Development, non-consumer-eligible semantic map** for V1.6 sections 15–28.

It composes existing material, layout, typography, form-factor, accessibility, and focus/motion authorities instead of replacing their values. It establishes semantic roles for:

- canvas, solid, raised, functional-glass, clear-glass, and overlay materials;
- bounded none/low/standard blur intent rather than arbitrary blur values;
- semantic depth roles from canvas through modal/context surfaces;
- 15 typography roles mapped to inherited type authorities;
- compact/medium/expanded/workspace/far-view/wearable typography environments;
- Comfortable, Standard, and Compact density with interaction-target floors owned by `tokens/layout.json`;
- touch, pointer, keyboard, directional, stylus, voice-focus, assistive-input, and mixed input presentation;
- press-feedback semantics and platform-adapter-owned tactile intents.

Critical reading, security/privacy decisions, complex forms, accessibility fallback, and high-information content may force solid or near-solid presentation. Reduced Transparency, large text, performance pressure, and unsupported backdrop effects may reduce visual richness before semantics or interaction correctness.

Candidate/reference token sources remain provenance inputs only; this map does not promote their historical lifecycle status. It also does not change V1.5.1 Stable values, consumer eligibility, downstream acceptance, release publication, deployment, or production state.


## V1.6 resilience and feedback Development semantic map

`tokens/glaze-v1.6-resilience-feedback.dev.json` is a **Development, non-consumer-eligible semantic map** for V1.6 sections 29–40.

It composes existing state, semantic-color, motion, material, loading, accessibility, focus, and material/type/input authorities into semantic roles for:

- ten distinct empty-state reasons rather than one generic empty screen;
- fully-online/offline/local-only/partial/sync/degraded connectivity presentation;
- indeterminate, determinate, step, background, sync, transfer, and processing progress;
- Passive, Informational, Actionable, Important, and Critical notification priorities;
- toast, persistent banner, inline status, and dialog surfaces;
- non-color destructive-action communication and confirmation semantics.

The map preserves caller/provider authority for recovery capability, connectivity truth, data safety, notification criticality, destructive intent, privacy, security, and authorization. It forbids invented recovery, timeout-based connectivity inference, fake progress, invented critical notifications, automatic destructive execution, and blanking usable stale content by default.

This map does not change Stable V1.5.1 values, consumer eligibility, downstream acceptance, release publication, deployment, or production state.


## V1.6 search, navigation, responsive, status, and authority Development semantic map

`tokens/glaze-v1.6-navigation-status.dev.json` is a **Development, non-consumer-eligible semantic map** for V1.6 sections 41–54.

It composes current layout, state, semantic-color, iconography, form-factor, accessibility, and resilience authorities into semantic roles for:

- stable search phases and partial-result continuity;
- primary-navigation stability and preserved task context;
- semantic responsive environments rather than raw-width-only behavior;
- single/dual/multi/overlay pane transitions and platform-owned posture/unsafe regions;
- RTL, mixed-direction, variable text expansion, locale-aware number/date formatting, and directional icon behavior;
- icon active/inactive/disabled/unavailable presentation with labels when meaning is unclear;
- standardized status and badge categories;
- truthful source/provenance presentation without implied ownership or authorization;
- privacy and security states whose truth remains owned by Privacy Shield, Wardveil Security, or another authoritative caller/provider;
- capability-state presentation that distinguishes Available, Unavailable, Unsupported, Restricted, Permission required, Temporarily unavailable, and Unknown without automatic permission requests or silent removal.

Unverified status claims use an explicit `status.unverified` role. The map does not infer provider precedence, navigation actions, privacy/security truth, permission, authorization, device identity, locale, or capability support.

This map does not change Stable V1.5.1 values, consumer eligibility, downstream acceptance, release publication, deployment, or production state.


## V1.6 complexity and component-systems Development semantic map

`tokens/glaze-v1.6-component-systems.dev.json` is a **Development, non-consumer-eligible semantic map** for V1.6 sections 60–70.

It composes current state, layout, material, semantic-color, motion, loading, accessibility, and prior V1.6 authorities into semantic roles for:

- seven bounded visual-complexity dimensions and Development reference budgets;
- active, idle-calm, and background energy presentation;
- minimum Default/Hover/Focused/Pressed/Selected/Disabled/Loading/Error component-state coverage;
- component nesting constraints that avoid nested transparency, repeated borders/padding, and conflicting elevation;
- required/optional/validation/read-only/save form presentation;
- Unsaved, Saving, Saved, Save failed, Conflict, and Offline pending persistence feedback;
- solid or near-solid dense-table presentation with accessible row/column semantics;
- labels, values, summaries, accessible descriptions, and table alternatives for charts;
- contrast/scrim/opacity/bounded-blur/protected-text media control protection;
- standardized scrollbar, overscroll, restoration, sticky, nested, and keyboard scrolling;
- subtle toolbar/status/inline/progress surfaces for nonblocking background work.

The complexity budget may simplify optional effects, but it may not remove semantic content, reduce accessibility, hide critical state, invent save/data/progress truth, or execute application work. Its numeric reference thresholds are Development guidance only and are not Stable production thresholds.

This map does not change Stable V1.5.1 values, consumer eligibility, downstream acceptance, release publication, deployment, or production state.


## V1.6 experience-governance Development semantic map

`tokens/glaze-v1.6-experience-governance.dev.json` is a **Development, non-consumer-eligible semantic map** for V1.6 sections 74–79 and 88–93.

It composes current layout, state, semantic-color, material, motion, iconography, and implemented V1.6 authorities into semantic governance for:

- progressive disclosure that keeps application-declared essential functionality visible;
- Primary, Secondary, Tertiary, Contextual, and Destructive action hierarchy;
- shared GoreeCloud application chrome and familiar common-operation behavior;
- semantic token categories and protected token domains;
- fail-closed presentation of capability, authority, privacy, security, connectivity, availability, and permission truth;
- minimum-necessary adaptation signals that reject personal content, private communications, browsing history, precise behavior, and unrelated app state;
- local-first resolution of ordinary appearance, accessibility, responsive behavior, skeleton loading, component state, focus, semantic color, and density;
- stable primary-action ordering unless an application supplies a strong task-related reason for recomposition;
- calm-default visual behavior;
- expressive effects that must improve at least one approved outcome such as hierarchy, readability, feedback, continuity, spatial understanding, state comprehension, or identity.

Reference dominant-action limits are Development guidance only. Protected semantic meaning, truth authority, privacy, permission, and consequential actions remain outside presentation authority.

This map does not change Stable V1.5.1 values, consumer eligibility, downstream acceptance, release publication, deployment, or production state.
