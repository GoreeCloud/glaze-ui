# Glaze UI 2.1 Candidate Contract

Status: **Candidate**  
Candidate line: **2.1.0-candidate.1**  
Current Stable remains: **2.0.0**  
Governing principle: **Make interaction feel tangible. Make every interface feel intentional. Make GoreeCloud beautiful.**

Glaze UI 2.1 is a refinement of the Glaze UI 2.0 identity, not a replacement for it. Nothing in this Candidate contract changes the current Stable consumer target until the normal promotion gate is completed with exact-revision, rendered, accessibility, resilience, native/platform, and visual-acceptance evidence as applicable.

## 1. Candidate objective

Glaze UI 2.1 turns the 2.0 visual and interaction identity into a more mature platform design system: precise, reusable, predictable, machine-readable, testable, accessible, performant, resilient, cross-platform, easy to adopt, difficult to implement incorrectly, and exceptionally refined.

The carried-forward signature remains ergonomic spatial hierarchy, Glaze Material, Connected Transformation, Adaptive Expression, content-first composition, reachability-first interaction, purpose-built form-factor adaptation, semantic tokens, strong accessibility, resilient rendering, native interaction patterns, consistent platform-state presentation, evidence-backed conformance, and exceptional visual craftsmanship.

## 2. Beauty and Visual Excellence

Beauty is a first-class requirement. A conforming production experience must aim to be beautiful, refined, elegant, polished, premium, calm, comfortable, cohesive, expressive, modern, purposeful, balanced, and distinctly GoreeCloud without sacrificing accessibility, readability, usability, performance, privacy, security, responsiveness, resilience, native behavior, user control, or information clarity.

**Visual Excellence** is a formal Candidate conformance dimension. It covers composition, proportion, alignment, spacing, typography, color harmony, contrast, surface hierarchy, material balance, optical balance, icon quality, motion quality, shape relationships, rhythm, density, depth, responsiveness, state transitions, attention hierarchy, and overall polish. Automated checks govern measurable properties; human visual review governs perceptual quality that cannot be reduced safely to numeric tests. A materially poor visual result may block release even when automated conformance passes.

Optical correction is permitted when strict mathematical equality produces inferior perceptual balance, but corrections must be intentional, bounded, documented where non-obvious, and must not weaken semantic or accessibility requirements.

Beauty should come from restraint and detail rather than excess. More blur, transparency, motion, color, rounding, decoration, or depth is not inherently better. Uncommon states—including hover, focus, pressed, disabled, loading, empty, error, sync, offline, menus, tooltips, dialogs, light/dark/deep-dark, and accessibility fallbacks—must receive the same craft discipline as primary states.

`VISUAL_EXCELLENCE.md` defines the Candidate review gate.

## 3. Lifecycle and normative documentation

The primary implementation contract must separate Stable, Candidate, Experimental, Planned, Deprecated, and Historical behavior. Historical rules remain available for migration, compatibility, rollback, audit, and provenance but must not be mixed into the current contract in ways that obscure active requirements.

`registry/lifecycle.json` is the machine-readable lifecycle authority introduced by this Candidate. Documentation and validation should consume it instead of independently restating lifecycle status wherever practical.

Stable 2.0 behavior remains Stable unless explicitly superseded by a later promoted release. Candidate 2.1 requirements must not be represented by consumers as Stable.

## 4. Machine-readable component contracts

Important components should converge on machine-readable semantic contracts. A contract may define semantic and material roles; typography; geometry; spacing; color roles; applicable states; touch and pointer targets; keyboard, focus, hover, press and selection behavior; motion and haptic roles; accessibility semantics; reduced-motion, reduced-transparency, increased-contrast, large-text and forced-color behavior; density; form-factor support; adaptive transformation; fallback behavior; native mappings; and visual-review requirements.

`schemas/component-contract.schema.json` establishes the Candidate schema. `contracts/components/navigation-capsule.json` is the first Candidate component contract and reference for additional contracts.

## 5. Conformance linting

Glaze UI conformance tooling should increasingly detect objective violations such as hard-coded color where semantic tokens are required, arbitrary radii, invalid material combinations, excessive high-intensity Glaze use, missing states, inadequate target sizes, missing accessibility preferences, inaccessible contrast, invalid semantic color or icon use, unsupported density/form-factor assumptions, and absent Glaze component mappings.

Tooling must distinguish objective violations from human-review recommendations. A subjective aesthetic recommendation must not masquerade as a deterministic machine failure unless a measurable rule actually exists.

`scripts/validate_glaze_2_1_candidate.py` validates the bounded Candidate foundation and lifecycle separation; it is not evidence that every 2.1 capability is implemented.

## 6. Glaze Material 2.1

The Stable 2.0 material hierarchy carries forward unchanged:

1. Canvas
2. Surface
3. Soft Glaze
4. Glaze
5. Deep Glaze
6. Live Glaze

**Content is solid. Interaction is glazed.** Canvas and Surface remain the default for reading, working, files, mail, documents, settings, tables, feeds, and administration. Soft Glaze, Glaze, Deep Glaze, and Live Glaze identify navigation, interaction, context, transience, elevation, direct manipulation, and ongoing activity according to role.

2.1 Candidate work adds deterministic bounded behavior for opacity, blur, tint, diffusion, saturation, refraction, optical distortion, directional highlight, borders, tonal separation, environmental influence, depth, lighting, interaction response, accessibility fallback, and performance fallback. Implementations must not use unrestricted effect combinations and claim equivalent material identity.

Material Budgets limit excessive use of Glaze, Deep Glaze, and Live Glaze, especially in content-heavy products. The Adaptive Optical Engine may respond to background complexity/luminance, foreground contrast, appearance, Material Clarity, Increased Contrast, Reduced Transparency, display capability, performance, state, surface size, ambient/context color, and interaction direction, but behavior must remain bounded by readability, accessibility, performance, and semantic hierarchy.

Material Clarity is formalized as **Clear → Balanced → Solid**. Balanced is the default. Solid replaces translucency with deliberate tonal, geometric, border, depth, and contrast hierarchy without changing task structure.

## 7. Geometry, color, type, spacing, and density

Core radius roles remain 4 Micro, 8 Small, 12 Standard, 16 Medium, 24 Large, 32 Hero, 50% Circular, and 999 Capsule. Nested surfaces should preserve concentric relationships where appropriate. Utility shapes prioritize predictable infrastructure; Expression Shapes may be organic, asymmetric, morphable, or dynamic only when they communicate meaningful media, illustration, progress, avatar, intelligence, hero, or special-state expression.

Color remains layered into Foundation, Identity, and Ambient roles. Identity derives from an Accent Seed with semantic roles such as Accent, Soft, Container, Strong, and Contrast. **Color the content freely. Tint the chrome selectively.** Light, Dark, and Deep Dark are independently tuned systems rather than inversion.

Suggested typography roles remain Display XL 64–72, Display 48–56, Headline XL 36–40, Headline 28–32, Title 22–24, Body Large 18, Body 16, Label 14, Caption 12. Core spacing remains 4, 8, 12, 16, 24, 32, 48, 64. Typography and whitespace must establish hierarchy before decorative complexity.

Density is formalized as **Comfortable, Standard, Compact, Far View** and coordinates row/control/icon sizes, typography, padding, spacing, menus, toolbars, tables, cards, and target sizes. Density adapts to form factor, input, window size, viewing distance, pointer precision, touch availability, preference, and task. Compact must remain accessible; Comfortable must remain purposeful.

## 8. Form-factor and navigation transformation

Mobile preserves Viewing, Working, and Glaze Action Zones and prioritizes touch, reachability, focused workflows, progressive disclosure, bottom-zone interaction, clear hierarchy, and comfortable targets. Tablet prioritizes multi-pane work, mixed touch/pointer input, posture/orientation change, drag-and-drop, and continuity. Desktop prioritizes keyboard, pointer, hover, context menus, resizable windows, persistent navigation, inspectors, multi-panel workspaces, multi-window interaction, and deliberate density. TV prioritizes distance viewing, directional focus, large targets, strong selection, Far View density, and must never depend on hover or touch.

Foldable behavior covers folded single-pane, dual-pane, half-open/tabletop, cover display, hinge avoidance, pane continuity, cross-pane dragging, and orientation transitions. Critical controls and sheets must not blindly span hinges or occlusions.

Components define semantic transformation across Mobile, Tablet, Desktop, Wide Desktop, TV, foldable, and resizable contexts. The navigation family remains **Navigation Capsule → Navigation Rail → Sidebar → Focus Dock** where appropriate.

Navigation Capsule 2.1 formalizes destination count, selection, labels/icons, expansion/compression, scroll response, safe area, material, reachability, accessibility, reduced motion, and larger-screen transformation. Search may transform from its source control into expanded/global search, a command palette, universal launcher, or contextual search workspace while preserving focus and spatial continuity.

## 9. Components and state completeness

Buttons use semantic roles such as Quiet, Soft, Glaze, and Emphasis; Emphasis remains scarce. Cards exist only where containment communicates structure and avoid nested rounded-rectangle stacks. Toolbars are compact, contextual, purposeful, and spatially grouped. Menus/popovers should remain connected to their invoking control. Sheets support Peek/Partial/Full where useful and may reduce corner geometry as they approach full screen. Toggles/sliders should feel physically connected to state while keeping accessible hit areas larger than visible geometry where needed.

Production components define every applicable state: Default, Hover, Focus, Pressed, Selected, Disabled, Loading, Indeterminate, Success, Information, Warning, Error, Destructive, Offline, Unavailable, Protected, Restricted, Syncing, and other relevant semantic states.

State is communicated through coordinated material, color, geometry, outline, typography, iconography, motion, haptics, and semantic labels. Important meaning must never depend on one sensory channel.

## 10. Connected Transformation, motion, physics, and haptics

Connected Transformation is a formal interaction grammar. Canonical families include Button→Menu, Button→Creation Surface, Search→Search Workspace, Chip→Filter Panel, Mini Player→Full Player, Notification→Activity Surface, Item→Detail, Toolbar Action→Contextual Panel, Navigation Destination→Workspace, and Live Surface→Persistent Activity Surface.

Each transformation specifies source, destination, spatial relationship, focus transfer, identity continuity, duration, spring behavior, interruption, reversal, reduced-motion alternative, and accessibility semantics. **Nothing teleports.** A connected transform must not be used when it creates ambiguity, delay, broken reading/focus order, unnecessary movement, unrelated conceptual linkage, overload, accessibility conflict, or obstruction. A fade or direct state change may be more correct.

Motion aligns with Glaze Motion semantics without making Experimental Glaze Motion a Stable dependency. Motion definitions describe purpose, duration envelope, easing/spring, distance, scale, deformation, opacity, material/depth transition, interruption, reduced-motion equivalent, and haptic relationship. Reusable timing roles include Instant, Fast, Standard, Emphasized; reusable spring roles include Restrained, Standard, Expressive, Spatial.

Direct manipulation—drag, drop, reorder, swipe, scroll, overscroll, snap, pan, zoom, resize, slider/toggle, window and pane movement—must remain immediate, predictable, interruptible, reversible where appropriate, and physically coherent. Semantic haptic roles may include Tap, Toggle, Selection, Threshold, Snap, Drop, Success, Warning, Error, Confirmation, and Protected Action when hardware permits.

## 11. Accessibility Resolution Matrix

2.1 Candidate work introduces a deterministic Accessibility Resolution Matrix for interactions among Reduced Motion, Increased Contrast, Reduced Transparency, Large Text, Show Boundaries, Touch Assistance, Forced Colors, Material Clarity, Accent personalization, and Expression level. Applications must not independently invent incompatible resolution behavior.

Reduced Transparency increases opacity while preserving intentional hierarchy. Increased Contrast strengthens text, borders, focus, surfaces, interaction states, and semantic distinction without merely darkening everything. Reduced Motion removes unnecessary spatial movement rather than only making it faster; direct manipulation still tracks user input where required. Large Text reflows and restructures layouts instead of clipping or shrinking critical information. Touch Assistance may enlarge interaction targets independently of visible control size. Important information is color-independent.

Accessibility modes must remain beautiful and intentional. They are alternate first-class renderings, not degraded afterthoughts.

## 12. Personalization and recipes

Controlled personalization may include Appearance, Accent Seed, Ambient Color, Material Clarity, Expression, and appropriate Density. Expression is formalized as **Calm → Balanced → Expressive** and may influence motion richness, transformation depth, ambient tint, shape variation, hero typography, material response, lighting, and spatial behavior. Personalization must never alter protected error, warning, destructive, success, security, privacy, focus, accessibility, or essential hierarchy semantics.

Official Glaze Recipes provide governed defaults without flattening product personality:

- **Productivity** — content clarity, moderate density, restrained motion, surface-first composition, Soft Glaze navigation, limited Deep Glaze, predictable toolbars.
- **Communication** — Live Surface integration, contextual action, presence, notification transformation, moderate expression, strong activity visibility.
- **Media** — rich ambient color, Glaze controls over content, media-aware material, connected player transformations, more expressive motion.
- **Administration** — higher density, restrained color, lower translucency, strong tables, precise keyboard interaction, strong semantic states.
- **Creative** — adaptive tools, contextual floating controls, direct manipulation, flexible workspaces, richer spatial interaction.

## 13. Intelligence and Live Surfaces

Intelligent experiences use the ordinary Glaze grammar and do not require a stereotypical glowing gradient. Intelligence presentation may be Ambient, Assisted, Conversational, or Agentic, but visual treatment does not create model, agent, memory, automation, or execution authority.

Live Surfaces represent ongoing upload, download, sync, backup, call, navigation, timer, recording, generation, playback, transfer, delivery, and similar processes. Identity should persist across application, Navigation Capsule, notification, lock screen, desktop task area, and system activity contexts where supported. Priority may consider user initiation, relevance, required attention, completion urgency, error, security/privacy impact, and foreground relationship. Glaze UI presents producer-authoritative state and never manufactures underlying truth.

## 14. Icons and platform-state presentation

A centralized System Icon Registry should provide canonical semantic identities for common actions and concepts. Icons may support Outline, Filled, Tinted, and Layered modes while preserving identity at full color, monochrome, compact/notification, badged, and high-contrast contexts. Icon linting should validate measurable optical size, safe zones, badge clearance, contrast, semantic color, monochrome/high-contrast behavior, stroke, small-size complexity, dimensions, color profile, and accessibility metadata; artistic quality remains a human review responsibility.

Glaze UI standardizes presentation—not authority—for Privacy Shield privacy/consent/data-use state, Wardveil protection/trust/threat/security state, Everkeep backup/recovery/preservation state, GoreeCloud Sync sync/conflict/offline state, GoreeCloud Identity authentication/account/device-trust state, and GoreeCloud Mesh coordination/governance/dependency/shared-activity state.

Local/cloud vocabulary should consistently distinguish Local only, Stored in GoreeCloud, Synced, Sync pending, Cloud only, Offline copy available, Backup protected, Not backed up, Conflict, and Unavailable so users do not have to infer data location.

## 15. Performance and graceful degradation

Rendering performance profiles are **Full, Balanced, Constrained, Minimal**. Profiles may alter blur quality, refraction, environmental/background sampling, Live Glaze complexity, shadows, motion, lighting, and advanced effects without changing semantic meaning.

Material fallback proceeds deliberately from **Advanced Glaze → Simplified Glaze → Tonal Surface → Solid Surface**. Motion fallback proceeds from **Connected Morph → Restrained Movement → Fade → Immediate State Change**. Basic usability, hierarchy, task completion, and Glaze identity must survive every fallback. Beauty must come from composition, type, geometry, spacing, and semantic color first; advanced graphics are enhancement.

## 16. Cross-platform implementation and reference flows

Android, Linux, Web, TV, tablet, foldable, and future targets may use different native technologies while preserving a shared semantic design contract. Native applications must feel intentionally designed for their platform; native primitives are mappings of Glaze semantics, not exemptions.

2.1 reference flows should cover Settings, File Management, Messaging, Mail, Media Playback, Global Search, Administration, Permissions, Privacy Controls, Security Warnings, Backup/Restore, Synchronization, Long-running Activity, Error/Recovery, and Multi-pane Workspace. Flows demonstrate material, components, motion, density, type, state, accessibility, responsive transformation, platform integration, and polish as one experience.

The acceptance matrix should span representative Mobile, Tablet, Desktop, Wide Desktop, TV; Light, Dark, Deep Dark; Reduced Motion, Reduced Transparency, Increased Contrast, Large Text/200%, Forced Colors; keyboard-only, touch-only, pointer; and constrained-performance conditions as applicable. Acceptance asks not merely whether a layout fits, but whether it remains coherent, purposeful, beautiful, and recognizably Glaze UI.

## 17. Regression, tooling, adoption, and visual review

Visual regression should detect unexpected geometry, spacing, material, color, typography, focus, responsive-layout, fallback, navigation, and platform-state changes. Not every pixel difference automatically fails; unexpected differences require intentional review. Interaction regression covers keyboard traversal/focus order, touch/pointer targets, navigation, menus/dialogs, Connected Transformation, drag-and-drop, resizing, reduced motion, form-factor transitions, and dynamic text.

A Glaze UI development inspector may expose component identity, material role, semantic color, typography, spacing, density, interaction state, motion role, accessibility mapping, target size, form-factor mapping, and platform-state source. Technical documentation should increasingly be generated from machine-readable definitions. Integration packages should provide appropriate combinations of tokens, components, icons, motion, accessibility, density, fallbacks, state presentation, references, tests, and validators.

Every adopting GoreeCloud application should record target Glaze version, form factors, densities, material capability, appearance, component mappings, accessibility evidence, motion mappings, platform-state mappings, conformance results, and visual-acceptance evidence. Consumer states include Current Stable aligned, Current Stable Adoption Candidate, Migration required, Evidence incomplete, Unsupported for target, and Development only. Historical conformance remains visible but cannot be mistaken for current conformance.

Major component and application releases require visual review covering finish, intentionality, hierarchy, proportion, material restraint, typography, icon quality, spacing/alignment, motion, accessibility-mode beauty, and distinct GoreeCloud character. Visual quality may block release.

## 18. Glaze UI signature and promotion boundary

A conforming experience should exhibit enough of the following to be unmistakably Glaze UI: large calm content areas; solid content-first surfaces; selective Glaze interaction islands; ergonomic control placement; concentric geometry; Connected Transformation; Adaptive Expression; disciplined color; expressive but controlled typography; purposeful depth and motion; semantic state communication; responsive form-factor transformation; strong accessibility; product individuality; and exceptional polish.

Blur, transparency, rounded corners, and spring animation alone do not constitute Glaze UI. Applications should feel like a family of premium products rather than copies of one template. Glaze UI provides the grammar; applications provide the personality; beauty is expected from both.

### Promotion gate

2.1 must not be promoted until:

- the Candidate lifecycle registry and machine-readable contracts are internally consistent and fail-closed;
- materially affected Stable regression suites remain passing;
- Candidate semantics have applicable implementation/reference evidence rather than documentation-only claims;
- accessibility-resolution and performance-fallback behavior is validated;
- representative form-factor/reference flows receive rendered and interaction acceptance;
- native/platform-specific behavior receives native or real-device evidence where browser/source evidence is insufficient;
- Visual Excellence review is completed by humans against representative primary, secondary, failure, accessibility, and fallback states;
- consumer migration guidance and compatibility impact are explicit; and
- exact-final-revision CI and normal GoreeCloud release governance pass.

Until that gate is complete, **2.0.0 remains the only current Stable Glaze UI consumer target and 2.1 remains Candidate.**