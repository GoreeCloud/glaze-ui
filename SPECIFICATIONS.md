# GLAZE UI V1.5 — Specifications

## Product identity

- **Official product label:** GLAZE UI V1.5 — Contextual + Capability Awareness
- **Machine version:** `1.5.1`
- **Lifecycle:** Stable
- **Consumer eligibility:** Yes, as a shared Glaze UI Stable release
- **Repository:** `GoreeCloud/goreecloud-glaze-ui`
- **Authoritative family contract:** `GLAZE_UI_V1_5.md`
- **Stable qualification scope:** `contracts/v1.5.1/stable-scope.json`
- **Stable acceptance record:** `acceptance/v1.5.1-stable.md`
- **Qualification-hardening record:** `GLAZE_UI_V1_5_1_HARDENING.md`
- **Lifecycle authority:** `registry/lifecycle.json`

V1.5.1 is the Stable qualification-hardening patch for the V1.5 Context + Capability Awareness line. It preserves the reviewed V1.5 presentation and authority implementation while closing the two shared qualification expansions intentionally deferred from V1.5.0.

## Runtime and Stable entrypoints

- Version authority: `VERSION`
- Web/material entrypoint: `css/glaze-v1.4.1.css`
- Runtime entrypoint: `js/glaze-v1.5.1.mjs`
- Immediate known-good Stable rollback runtime: `js/glaze-v1.5.0.mjs`
- Stable authority gate: `scripts/verify_glaze_v1_5_1_stable.mjs`
- Consumer registry: `consumers/registry.json`

The V1.5.1 runtime inherits the reviewed V1.5.0 Stable behavior and promotes Stable patch identity and qualification closure without changing the reviewed presentation or operational-authority boundary.

## Stable V1.5 requirements

V1.5 extends the inherited V1.4.1 Optical Intelligence foundation with governed Context + Capability Awareness. The Stable contract requires:

- semantic context normalization across governed domains;
- capability-state grammar with provenance;
- explicit provider authority/domain ownership;
- fail-closed handling of provider ownership conflicts;
- Privacy Shield ownership of privacy/data-use authorization truth where applicable;
- contextual composition and presentation-density adaptation;
- accessibility precedence over visual richness;
- runtime-pressure presentation-cost reduction without capability-truth modification;
- connectivity, window-state, posture, and constrained-runtime continuity;
- capability-aware navigation and controls;
- stable primary-action ordering with predictable contextual adaptation of non-primary actions;
- explicit unavailable/degraded explanations and recovery metadata;
- graceful user-initiated fallback suggestions without automatic fallback execution;
- privacy-safe explainable diagnostics;
- inherited V1.4.1 optical-capability integration;
- unified Context + Capability Resolution for developer-facing presentation decisions.

## Authority boundary

Glaze UI remains presentation-only. It does not infer authorization, grant consent or permission, automatically request permission, automatically navigate because context changes, automatically execute consequential actions, or automatically execute fallback actions.

Privacy Shield, Wardveil Security, applications, services, platforms, policy, identity, device/runtime, and other authoritative providers retain their own truth domains. Provider ownership conflicts fail closed rather than being resolved through inferred precedence.

## V1.5.1 qualification boundary

The exact V1.5.1 Stable qualification scope is defined by `contracts/v1.5.1/stable-scope.json`.

V1.5.1 retains the sixteen obligations accepted for V1.5.0 and adds two independently reviewed obligations:

1. `performance-representative-budget` — accepted for the reviewed Zorin OS 17.3 / Firefox 156.0 / Lenovo IdeaPad 3 15IIL05 environment.
2. `platform-posture-continuity` — accepted for the approved Pixel Fold Android Emulator target runtime under `GCU-ADR-GLAZE-V151-POSTURE-TR-001`.

The complete shared Stable qualification therefore contains eighteen accepted obligations. These claims remain bounded to their reviewed environments and do not automatically establish downstream application performance, physical-device, posture, deployment, or production acceptance.

## Evidence continuity

The reviewed V1.5 presentation and authority implementation remains anchored to exact revision `ee1032a0822ab8e103f8afe48e5c1859fde65cc9`.

The two V1.5.1 qualification observations remain bound to exact Development revision `5b59d0e36950d737dba35b58ae58058684e0831b`.

Stable promotion preserves those evidence boundaries through fail-closed source-impact continuity. Evidence is not relabeled as if it were performed on later release-metadata revisions.

## Consumer boundary

V1.5.1 is the required shared Glaze UI target recorded by the current consumer registry. No downstream GoreeCloud application becomes conformant, Stable, deployed, production-eligible, or production-ready automatically.

Every applicable consumer must complete fresh repository-local exact-revision V1.5.1 adoption and acceptance for its supported platforms.

## Publication and deployment boundary

Shared Stable source/lifecycle authority does not by itself establish an immutable `v1.5.1` tag, GitHub Release publication, deployment, production acceptance, or downstream consumer acceptance. Those remain separate governed transitions.

## Development successor boundary

Development-only successor language, contracts, schemas, tokens, validators, and reference inputs may coexist in this repository. They remain non-consumer-eligible and do not alter V1.5.1 Stable authority unless separately promoted through the governed lifecycle.

`GLAZE_UI_V1_6_PLANNED.md` records the planned V1.6 successor requirements, centered on semantic skeleton/loading behavior, state clarity, accessibility, motion, materials, responsive continuity, performance adaptation, diagnostics, conformance metadata, adoption profiles, and evidence-backed acceptance.

The first bounded V1.6 Development implementation foundation is defined by `contracts/v1.6/loading-skeleton.dev.json`, `schemas/v1.6-loading-skeleton.schema.json`, `tokens/glaze-v1.6-loading.dev.json`, and `js/glaze-v1.6-loading.dev.mjs`. It implements sections 1–4 as a non-consumer-eligible loading/skeleton source foundation with configurable loading escalation, quiet-window behavior, skeleton primitives and motion modes, accessibility precedence, truthful progress handling, stale-content preservation, bounded optimistic presentation, motion-fatigue protection, and presentation-only authority boundaries. This Development implementation does not establish Candidate or Release Candidate status, Stable qualification, consumer eligibility, downstream adoption, deployment, production acceptance, or publication.

The second bounded V1.6 Development foundation is defined by `contracts/v1.6/state-accessibility.dev.json`, `schemas/v1.6-state-accessibility.schema.json`, `tokens/glaze-v1.6-state-accessibility.dev.json`, `js/glaze-v1.6-state-accessibility.dev.mjs`, and the aggregate `js/glaze-v1.6-development.mjs`. It implements sections 6–9 and 55–59 with a 26-state semantic grammar, protected semantic color roles, 13 composable accessibility profiles, explicit Disabled/Unavailable/Restricted/Unsupported/Permission-required distinctions, four visual-performance levels, authoritative runtime-pressure adaptation, anti-jitter stability/dwell/hysteresis behavior, and privacy-safe adaptation diagnostics. Accessibility retains precedence over visual richness, performance adaptation cannot modify capability truth, and the V1.6 aggregate remains Development/non-consumer-eligible rather than a release runtime.

The third bounded V1.6 Development foundation is defined by `contracts/v1.6/focus-motion.dev.json`, `schemas/v1.6-focus-motion.schema.json`, `tokens/glaze-v1.6-focus-motion.dev.json`, and `js/glaze-v1.6-focus-motion.dev.mjs`, and is composed into the Development aggregate. It implements sections 10–14 and 71–73 with material-aware focus visibility and restoration semantics; 17 semantic motion families; motion magnitude/hierarchy constraints; interruptible user-driven transitions; bounded fatigue budgets; 14 reusable microinteraction intents; same-identity state continuity; and focus/scroll-preserving content replacement. Reduced Motion simplifies or removes nonessential travel, final semantic state never depends on an animation completing, and this V1.6 semantic motion work does not promote the separately governed Glaze Motion Experimental foundation.

The fourth bounded V1.6 Development foundation is defined by `contracts/v1.6/material-type-input.dev.json`, `schemas/v1.6-material-type-input.schema.json`, `tokens/glaze-v1.6-material-type-input.dev.json`, and `js/glaze-v1.6-material-type-input.dev.mjs`, and is composed into the Development aggregate. It implements sections 15–28 with context-aware material strengthening, semantic blur/depth roles, solid-surface boundaries for critical/readability-sensitive content, 15 semantic typography roles, environment/text-scale/language-aware type adaptation, explicit 200%-class large-text reflow behavior, Comfortable/Standard/Compact density with protected interaction floors, task-continuous input adaptation, hover-as-enhancement, immediate press feedback, and platform-mapped tactile intents. Existing token/value authorities remain the source of values; this tranche does not create hardware haptic mappings, inspect private background content, infer locale from content, or weaken accessibility/Stable lifecycle boundaries.

The fifth bounded V1.6 Development foundation is defined by `contracts/v1.6/resilience-feedback.dev.json`, `schemas/v1.6-resilience-feedback.schema.json`, `tokens/glaze-v1.6-resilience-feedback.dev.json`, and `js/glaze-v1.6-resilience-feedback.dev.mjs`, and is composed into the Development aggregate. It implements sections 29–40 with ten reason-specific empty states; structured privacy-safe error presentation; caller-authorized recovery actions; seven first-class connectivity/sync states; stale-content and background-refresh continuity; safe reversible optimistic interaction; seven truthful progress modes; five notification priorities; toast/banner/inline/dialog governance; keyboard/focus-safe dialogs; and non-color destructive-action protection. Recovery capability, connectivity truth, data safety, criticality, and destructive intent remain caller/provider-owned, and no recovery, focus, destructive, permission, or other consequential action is executed automatically by the presentation resolver.

The sixth bounded V1.6 Development foundation is defined by `contracts/v1.6/navigation-status.dev.json`, `schemas/v1.6-navigation-status.schema.json`, `tokens/glaze-v1.6-navigation-status.dev.json`, and `js/glaze-v1.6-navigation-status.dev.mjs`, and is composed into the Development aggregate. It implements sections 41–54 with stable multi-provider search-result continuity; preservation of scroll/selection/expanded/filter/query/pane task context; stable primary navigation under transient capability changes; responsive composition driven by semantic environment, viewing distance, input, posture, density, task, and accessibility rather than width alone; deterministic pane transitions; platform-owned unsafe-region/posture handling; localization/RTL/text-expansion resilience; icon-label and directional-correctness rules; standardized status/badge/source presentation; and fail-closed privacy, security, and capability controls. Unverified status claims resolve to an explicit Unverified presentation rather than being upgraded or coerced into another positive state, and Glaze never manufactures provider precedence, ownership, authorization, privacy, security, or capability truth.

The seventh bounded V1.6 Development foundation is defined by `contracts/v1.6/component-systems.dev.json`, `schemas/v1.6-component-systems.schema.json`, `tokens/glaze-v1.6-component-systems.dev.json`, and `js/glaze-v1.6-component-systems.dev.mjs`, and is composed into the Development aggregate. It implements sections 60–70 with a seven-dimension visual-complexity budget; energy-aware idle/power/thermal simplification; minimum reusable-component state completeness; composition rules that reject nested transparency, repeated borders/padding, and conflicting elevation by default; required/optional/validation/read-only/save form semantics; six authoritative save states; conservative dense-table materials and accessible row/column semantics; chart nonvisual-alternative requirements; protected media-control legibility; keyboard/restorable/nested scroll behavior; and nonblocking background-work presentation. Development reference thresholds guide optional-effect simplification only and do not establish Stable production thresholds; semantic content, accessibility, state truth, data truth, save truth, and task execution remain outside the complexity budget and presentation resolver's authority.

The eighth bounded V1.6 Development foundation is defined by `contracts/v1.6/experience-governance.dev.json`, `schemas/v1.6-experience-governance.schema.json`, `tokens/glaze-v1.6-experience-governance.dev.json`, and `js/glaze-v1.6-experience-governance.dev.mjs`, and is composed into the Development aggregate. It implements sections 74–79 and 88–93 with progressive disclosure that cannot hide application-declared essential functionality; Primary/Secondary/Tertiary/Contextual/Destructive action hierarchy; common GoreeCloud application-chrome and operation familiarity requirements; semantic-token expansion and protected-token override blocking; fail-closed capability/authority/privacy/security/connectivity/availability/permission presentation; minimum-necessary adaptation signal filtering; local-first resolution for ordinary appearance/accessibility/responsive/loading/state rendering; stable primary-action ordering unless a strong task-related reason is supplied; calm-default presentation; and a restraint test requiring every expressive effect to improve hierarchy, readability, interaction feedback, continuity, spatial understanding, state comprehension, or identity. Presentation remains unable to manufacture truth, collect private content for visual adaptation, grant permission, or execute actions.

The ninth bounded V1.6 Development foundation is defined by `contracts/v1.6/performance-diagnostics.dev.json`, `schemas/v1.6-performance-diagnostics.schema.json`, `tokens/glaze-v1.6-performance-diagnostics.dev.json`, and `js/glaze-v1.6-performance-diagnostics.dev.mjs`, and is composed into the Development aggregate. It implements section 5 and sections 80–87 with partially useful/early-interactive perceived-performance behavior; privacy-minimized developer diagnostics; ten accessibility diagnostic dimensions; skeleton diagnostics that require caller/governance thresholds instead of inventing duration or shimmer limits; a deterministic 14-scene visual-regression matrix; semantic-regression checks that preserve meaning independently of appearance; evaluation of caller-supplied measurements against the approved Glaze UI Performance Budget v1.0 including refresh-adaptive frame limits; layout-stability checks that never invent a numeric shift budget; and explicit blur/morph/skeleton/environmental/transition degradation chains that preserve meaning and usability. Static validation does not manufacture real measurements, screenshots, native/device evidence, assistive-technology evidence, release acceptance, or lifecycle promotion.

The tenth bounded V1.6 Development foundation is defined by `contracts/v1.6/conformance-adoption.dev.json`, `schemas/v1.6-conformance-adoption.schema.json`, `tokens/glaze-v1.6-conformance-adoption.dev.json`, and `js/glaze-v1.6-conformance-adoption.dev.mjs`, and is composed into the Development aggregate. It implements sections 94–97 with an advisory Consistency Inspector spanning tokens, colors, typography, spacing, materials, focus, motion, skeletons, component states, accessibility, and loading; reusable component conformance metadata for states, accessibility modes, form factors, motion, fallbacks, and performance expectations; explicit application capability statuses of Implemented, Partially implemented, Unsupported, Not applicable, and Awaiting acceptance; and exact-revision V1.5.1 migration-continuity checks for semantic colors, accessibility precedence, contextual/capability awareness, authority boundaries, graceful fallback, continuity, and privacy-safe diagnostics. Shared Glaze lifecycle state never grants application adoption, component metadata never substitutes for runtime evidence, the inspector never modifies source automatically, and prior acceptance is never rebound to a new revision.

The eleventh bounded V1.6 Development foundation is defined by `contracts/v1.6/acceptance.dev.json`, `schemas/v1.6-acceptance.schema.json`, `acceptance/v1.6-development.md`, and `js/glaze-v1.6-acceptance.dev.mjs`, and completes Development source representation of planned sections 98–100. It defines 24 fail-closed qualification lanes, requires exact-revision evidence references, rejects stale/revision-mismatched/unsupported evidence, requires justification for not-applicable dispositions, records the eight proposed V1.6 core pillars, and encodes the governing principle that transient and failure states must be as intentionally designed as the final interface. A complete matrix may become ready for governed qualification review, but it does not grant Candidate, Release Candidate, Stable, consumer, deployment, or production status automatically. The durable Development acceptance record begins unverified for a future frozen qualification revision and must be populated only from actual evidence.

Acceptance-control hardening `1.6.0-dev.12` strengthens the same section 98–100 Development foundation without changing its planned scope. Evidence is now modeled as required groups rather than a single allowed evidence type: an applicable lane is verified only when every required group is satisfied on the same exact reviewed revision. Accessibility requires machine evidence plus human or assistive-technology evidence; Reduced Motion, Reduced Transparency, Increased Contrast, and large text require machine evidence plus rendered or human evidence; keyboard navigation requires machine plus human evidence; responsive layout and layout stability require both machine and representative non-machine evidence; privacy/authority boundaries require machine plus human review; regression testing requires machine plus rendered evidence; and representative rendering requires rendered evidence plus device or human review. Partial groups remain unverified and never imply lifecycle promotion.

The first V1.6 exact-source qualification checkpoint is bound to frozen Development source revision `c7509c79256b04b0aa67cb9dd0737d7588e0ae4a`. GitHub Actions run `35345027816`, job `105599478986`, materialized that exact revision and passed all implemented V1.6 Development validators plus the V1.5.1 Stable-authority verifier. The durable machine evidence record is `acceptance/v1.6-machine-evidence.json`. Machine evidence fully verifies 9 lanes, supplies only one required group for 11 additional multi-group lanes, and leaves Assistive Technology, Form-factor Transitions, Performance, and Representative Rendering untouched. The resulting matrix remains 9 verified / 15 unverified, is not qualification-complete, and is not ready for governed qualification review.

The second V1.6 exact-source qualification checkpoint adds bounded rendered-browser evidence without rebinding the frozen Development source. GitHub Actions run `35348330585` passed verification job `105610140264` and rendered capture job `105610194447`; durable evidence is preserved in `acceptance/v1.6-rendered-evidence.json` with artifact `10549115165` and digest `sha256:dbd9d89353b630eae781210ba334cfcf1288189533a27f70931facee1b245506`. Combined with machine evidence, this checkpoint verifies 16 lanes and leaves 8 unverified. It does not claim human, assistive-technology, device/native-platform, representative-performance, or regression-baseline acceptance.

The third V1.6 exact-source qualification checkpoint establishes bounded rendered regression evidence for the same frozen source. PR #258 merged the regression control at `b1f8575d6ed9199a7eb130f919680376c2e74d14` from exact tooling head `fe471447d37ea800d03be438e1126f0840f89000`. GitHub Actions run `35352215130` passed verification job `105622807547` and rendered-regression comparison job `105622931820`; artifact `10550685472` has digest `sha256:5c4058fba12969fe1c95c523f5f9cd4fc1fb846cc2b3aaab4b2ba84c9034839d`. The control preserves prior rendered scene semantics exactly and requires two fresh normalized captures to match by decoded-pixel SHA-256 for all nine scenes with zero pixel tolerance. Durable evidence is recorded in `acceptance/v1.6-regression-evidence.json`. Combined machine, rendered-browser, and rendered-regression evidence verifies 17 of 24 lanes and leaves 7 unverified; qualification remains incomplete and not ready for governed qualification review. V1.5.1 remains current Stable and V1.6 remains Development/non-consumer-eligible.
