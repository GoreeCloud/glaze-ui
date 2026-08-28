# Glaze UI 2.0 Component Contract

Glaze UI 2.0 standardizes shared semantics and interaction quality without forcing GoreeCloud products into identical composition. The current grammar is governed by **Make interaction feel tangible**: content is stable and readable; controls communicate relationship through Glaze Material, shape, motion, depth, and connected transformation.

## Universal component rules

Every directly actionable component must expose a clear accessible name, visible focus, predictable disabled/loading state, non-color-only semantics, and an effective interaction region of at least **48px** in the 2.0 reference unless a platform-native control provides an equal or safer target. TV reference targets remain at least **56px**. Component semantics, accessible hit regions, and task completion must survive reduced motion/transparency, increased contrast, forced colors, unsupported blur/backdrop effects, and effects-free operation.

Persistent field labels, associated help/error relationships, checked/selected state, determinate progress semantics, and native accessibility behavior remain mandatory.

## Glaze Material

Current 2.0 hierarchy:

1. **Canvas** — main background/workspace.
2. **Surface** — cards, lists, documents, content containers.
3. **Soft Glaze** — persistent navigation and secondary controls.
4. **Glaze** — floating controls and navigation.
5. **Deep Glaze** — menus, expanded controls and popovers.
6. **Live Glaze** — actively manipulated, focused, hovered, dragged, resized, spoken-to, or ongoing interactive surfaces.

Global clarity is Clear / Balanced / Solid. Readability overrides optical effect. Ordinary content stays on Canvas/Surface; glass-like effects are not universal card decoration.

### legacy 1.x compatibility

The retained 1.x regression layers still contain **Functional Glass** and **Clear Glass**, plus Canvas/Solid/Raised/Overlay terminology. These names remain historical compatibility semantics for migration and permanent regression testing only. Functional Glass historically represented functional chrome and Clear Glass historically represented controls over rich media. New and migrated 2.0 work uses the current Glaze Material hierarchy above.

## Shape and expression

Use the 2.0 radius scale `4 / 8 / 12 / 16 / 24 / 32 / 50% / 999`, concentric geometry, and role-driven utility/expression shapes. Expression communicates importance rather than decorating every surface. Calm/Balanced/Expressive personalization may tune visual intensity without changing semantics or accessibility.

## Buttons and action groups

Button roles are **Quiet, Soft, Glaze, Emphasis**. Emphasis is scarce. Physical press response may contract, pull a highlight toward the interaction point, increase optical density, provide optional haptics, and spring back, but effective targets remain stable and reduced-motion mode removes nonessential transformation.

Button groups may reallocate visual space while preserving semantic, reading, and focus order. Destructive meaning must not depend on color alone.

## Fields, inputs, and selection controls

Prefer **native platform controls** when they provide stronger semantics and ergonomics. Every editable field has a persistent label; placeholder text is supplementary. Textareas preserve readable reflow. Search may morph from its invoker but keeps platform keyboard/screen-reader/autofill behavior.

Checkbox, radio, toggle, picker, slider, chip, segmented control, and tab state must be programmatically exposed. A switch represents an immediate binary setting. Sliders may enlarge visible or effective touch geometry during direct manipulation while preserving accessible values and targets.

## Navigation

Phone primary navigation may use the **Navigation Capsule**. Its selected destination may expand, forward reading may compress surrounding chrome, and reverse scrolling may expand it; compression must never shrink the effective target below the 48px floor.

The same navigation concept transforms by environment: Tablet rail, Desktop sidebar, TV focus-driven dock, wearable compact rotational navigation, or spatial floating control surface. Components transform rather than merely resize.

## Connected Transformation

Connected Transformation is a signature pattern. An invoker and related destination should preserve source, direction, relationship, and state. Use native View Transition/shared-element mechanisms where appropriate; when unavailable, perform the semantic state change immediately and preserve continuity without blocking task completion. Nothing teleports merely for visual convenience.

## Cards, lists, toolbars, menus, popovers, and sheets

Cards contain independent or meaningfully grouped objects; nested cards are uncommon. Lists prioritize scanability and generous targets. Toolbars are compact contextual control islands. Menus/popovers emerge from their source control when possible. Phone sheets support Peek / Partial / Full states and may reduce radius as they approach fullscreen.

## Live Surfaces and progress

A Live Surface represents an ongoing process such as upload, transfer, navigation, timer, delivery, generation, recording, call, media playback, download, or synchronization. It may move across contexts while remaining recognizably one object. Presentation must never imply freshness, progress, completion, security, privacy, resilience, or coordination truth beyond producer evidence.

## Foldable layout

Foldables are first-class. Interactive content must not blindly span hinges/folds when pane-aware composition is safer. Hinge exclusion regions remain noninteractive; orientation/posture changes preserve task state, reading/focus order, and critical actions.

## Wearable mapping

Wearable UI is glance-first and is not a shrunken phone UI. Compact rotational navigation keeps one current/focusable item when roving focus is used, preserves a 48px reference floor, and retains an equivalent non-rotary task path where the native platform permits one. Host-managed surfaces and physical-device input require consumer-specific native acceptance.

## Spatial mapping

Spatial anchored surfaces, control volumes, environmental panels, and floating toolbars use depth only as supplemental hierarchy. Perspective must not reduce rendered interactive regions below the 48px floor; the reference therefore uses a larger nominal spatial target where needed. Full depth-free/flat fallback must remain semantically identical and operable.

## Motion and haptics

Utility motion is 100–180ms, Fluid 180–400ms, Expressive 400–700ms; implementation aliases are 140/280/520ms. Physical interactions prefer springs. Reduced motion substitutes shorter fades/restrained position changes and preserves direct manipulation.

Haptics may use tiny tap pulses, toggle snaps, selection ticks, drag-threshold notches, cushioned drops, restrained error double-pulses, and soft success confirmation. No essential meaning may depend on haptics.

## Accessibility and resilience

Large text reorganizes instead of clipping. Increased contrast strengthens boundaries/separation. Reduced transparency increases opacity. Color independence is mandatory. Show Boundaries may add explicit interactive outlines. Touch Assistance increases effective hit regions independently from visible size. The system remains usable without blur, translucency, shaders, complex animation, or GPU effects.

## Intelligence and authority

Prompt fields, assist surfaces, generation state, source surfaces, and agent-activity presentation use normal Glaze component grammar. Glaze UI is presentation-only: it creates neither execution authority nor domain truth. Privacy Shield, Wardveil Security, Everkeep, GoreeCloud Mesh, and application logic remain authoritative for their respective substantive state.
