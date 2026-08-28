# Glaze UI 2.0 Candidate — Enforced Design Contract

## Authority and lifecycle

This document is the implementation-facing source contract for the GoreeCloud administrator-approved Glaze UI upgrade declared on August 28, 2026.

- **Design-contract status:** Enforced for active Glaze UI design and development.
- **Lifecycle status:** Candidate.
- **Candidate semantic version:** 2.0.0.
- **Last validated Stable implementation baseline:** Glaze UI 1.6.0.
- **Production boundary:** this Candidate does not become a Stable production dependency until the normal source, rendered, accessibility, resilience, compatibility, migration, exact-revision CI, and release-promotion gates pass.
- **Consumer boundary:** affected GoreeCloud interfaces are migration-required for this contract as active development proceeds, but no consumer may claim Glaze UI 2.0 conformance or production acceptance before Candidate promotion and application-specific acceptance.

The major-version Candidate boundary is intentional: this contract changes established material levels, geometry, motion timing and interaction grammar, personalization, adaptive layout semantics, and component families rather than making a backward-compatible patch to 1.6.

The governing sentence is:

> **Make interaction feel tangible.**

The defining identity is:

**ergonomic spatial hierarchy + Glaze Material + connected transformation + adaptive expression**

Glaze UI is not an imitation of another platform. Product-specific personality remains expected inside a shared GoreeCloud interaction grammar.

## 1. Core philosophy

Glaze UI 2.0 is governed by six principles:

1. **Content is solid. Interaction is glazed.** Ordinary documents, photos, feeds, settings, lists, dashboards, canvases, and content live on Canvas/Surface roles. Navigation, transient controls, menus, floating toolbars, command surfaces, media controls, selection controls, and contextual actions use Glaze Material when appropriate.
2. **Reach before decoration.** On phones, information gravitates upward, frequent actions downward, contextual actions toward their source object, and destructive/infrequent controls remain secondary.
3. **Expression communicates importance.** Size communicates importance; shape communicates category/state; color communicates meaning/emphasis; motion communicates relationship; depth communicates interaction potential.
4. **Interfaces behave like connected objects.** Controls should transform into related menus, players, palettes, expanded activities, filter panels, and sheets rather than teleport between unrelated surfaces.
5. **Comfort beats density by default.** Comfortable composition is the default; compact/dense modes exist for genuine information-density needs.
6. **One system, many personalities.** Products remain recognizably Glaze without becoming visually identical.

## 2. Glaze Material

Glaze Material is a computational interaction surface, not generic transparent glass. Its implementation may combine translucency, blur, tint, optical distortion, directional highlights, depth, environmental color influence, physical response, and motion while prioritizing readability.

The normative levels are:

| Level | Name | Typical role |
| ---: | --- | --- |
| 0 | Canvas | Main background or workspace |
| 1 | Surface | Cards, lists, content containers |
| 2 | Soft Glaze | Persistent navigation and secondary controls |
| 3 | Glaze | Floating controls and navigation |
| 4 | Deep Glaze | Menus, expanded controls, popovers |
| 5 | Live Glaze | Actively manipulated, focused, hovered, dragged, resized, spoken-to, or dynamic surfaces |

This supersedes the former Canvas/Solid/Raised/Functional Glass/Clear Glass/Overlay hierarchy for Glaze UI 2.0 work. The prior hierarchy remains historical 1.x evidence only.

## 3. Adaptive optical behavior

Material behavior must respond to context without sacrificing comprehension:

- more background complexity increases material opacity;
- quieter backgrounds may permit greater translucency;
- higher-contrast or reduced-transparency modes decrease transparency;
- larger components gain visual weight;
- press highlights may move toward the interaction point;
- moving components may receive restrained internal-light response.

The global clarity model is **Clear — Balanced — Solid**. It modifies material rendering without changing information architecture or semantic structure.

## 4. Geometry

Glaze UI uses soft concentric geometry: inner curves visually relate to the enclosing shape instead of choosing arbitrary radii.

Core radius scale: `4 / 8 / 12 / 16 / 24 / 32 / 50% / 999`.

Two shape families are normative:

- **Utility shapes:** rounded rectangles, capsules, circles, sheets, panels.
- **Expression shapes:** organic, asymmetric, morphable, composed, or animated forms reserved primarily for media, illustration, progress, avatars, intelligence features, special states, and expressive experiences.

## 5. Color system

Glaze UI 2.0 uses three layers:

- **Foundation colors:** Canvas, Surface, Surface Raised, Surface Sunken, Border, Text Primary, Text Secondary, Text Muted.
- **Identity colors:** each product supplies an Accent Seed that derives Accent, Accent Soft, Accent Container, Accent Strong, and Accent Contrast roles.
- **Ambient colors:** nearby content may softly influence Glaze chrome without replacing semantic state colors.

Rule: **Color the content freely. Tint the chrome selectively.**

Semantic truth remains producer-authoritative. Glaze UI presentation cannot manufacture Privacy Shield, Wardveil Security, Everkeep, GoreeCloud Mesh, or application-state claims.

## 6. Appearance

Light and dark appearances have distinct material tuning; dark is not an inversion of light. Deep Dark is an optional appearance for displays capable of very dark blacks. Elevated Glaze surfaces must remain distinguishable from a black canvas.

## 7. Typography

Typography is a hierarchy system, not decoration. Prefer a variable typeface when an approved local/native font can provide weight, width, optical-size, and emphasis variation without remote runtime delivery.

Suggested semantic scale:

- Display XL: 64–72
- Display: 48–56
- Headline XL: 36–40
- Headline: 28–32
- Title: 22–24
- Body Large: 18
- Body: 16
- Label: 14
- Caption: 12

Scale may respond to semantic importance and form factor.

## 8. Spacing

Use a four-point base grid. Primary values are `4 / 8 / 12 / 16 / 24 / 32 / 48 / 64`. Spacing must be semantic/tokenized rather than chosen ad hoc per component.

## 9. Mobile layout

Mobile composition has three behavioral zones:

- **Viewing Zone** — understanding and context;
- **Working Zone** — direct manipulation and content controls;
- **Glaze Action Zone** — frequent reachable actions.

These are behavioral regions, not fixed pixel bands.

## 10. Adaptive layouts

Components transform across environments rather than merely resizing. A navigation concept may become a phone bottom floating capsule, tablet rail, desktop sidebar, television focus dock, wearable compact rotational navigation, or spatial floating control surface.

## 11. Navigation Capsule

The primary phone navigation pattern is a floating Navigation Capsule. The selected destination may expand while inactive destinations remain compact. Forward reading can compress navigation; reverse scrolling can expand it. The navigation surface should become visually quieter when content deserves attention.

## 12. Search

Search is a navigation state. It should expand from its invoking control where possible. On larger displays, the same grammar may map to global search, a command palette, universal launcher, or contextual search.

## 13. Buttons

Four button roles are normative: **Quiet, Soft, Glaze, Emphasis**. Emphasis must remain scarce.

A pressed Glaze button may contract, move its highlight toward the touch point, become optically denser, trigger restrained haptic confirmation, and spring back. Interaction physics replace opacity-only feedback.

## 14. Button groups

Adjacent controls may behave as one flexible physical system: selected controls can grow while neighbors compress or shift. Semantic order and accessible hit targets must remain stable.

## 15. Cards

Contain only when containment communicates something. Cards are appropriate for independent objects, draggable items, distinct states, grouped information, or interactive modules. Card levels are Flat, Tonal, Raised, and Interactive Glaze. Nested cards should be uncommon.

## 16. Lists

Lists prioritize scanability, touch-area generosity, meaningful secondary text, restrained icon use, alignment, and predictable control placement.

## 17. Toolbars

Toolbars are compact, floating, contextual Glaze control islands. Related controls may visually attract; unrelated controls remain spatially separated.

## 18. Menus and popovers

Menus emerge from their originating control. During transition, the invoker and expanded menu may temporarily read as one connected Glaze object.

## 19. Sheets

Phone sheets support Peek, Partial, and Full states. Radius may reduce toward fullscreen. Where appropriate, the invoking control stretches into the sheet to preserve continuity.

## 20. Toggles

Off is neutral/tonal; On is accent-treated. Dragging may subtly deform the thumb/track relationship while preserving platform-native accessibility semantics.

## 21. Sliders

Slider thumbs may behave like droplets along a rail. Touch enlarges the effective target and may enlarge the thumb; important increments may provide tactile feedback; settling should use soft spring behavior. Visible size may remain smaller than the effective touch region.

## 22. Iconography

Icons are geometric, friendly, optically balanced, slightly softened, variable, and animatable. Modes are Outline, Filled, Tinted, and Layered. Related states should transform when appropriate: play→pause, menu→close, bookmark→saved, volume→muted.

## 23. App icons

App icons use three conceptual layers: Highlight/Glaze, Symbol/Identity, Base/Color Field. They may adapt to appearance, accent, hover/focus, depth capability, and environmental light. The central mark must remain recognizable in monochrome.

## 24. Motion

Core rule: **Nothing teleports.** Objects expand, contract, merge, split, flow, spring, follow, and settle.

Motion families:

- **Utility:** 100–180 ms for hover, focus, tiny state changes, highlights.
- **Fluid:** 180–400 ms for navigation, menus, cards, sheets, panels.
- **Expressive:** 400–700 ms for onboarding, major transformations, creative tools, hero/immersive moments.

Physical interactions should prefer spring parameters to rigid easing curves. Reduced-motion behavior substitutes simpler shorter transitions and preserves direct manipulation semantics.

## 25. Connected Transformation

Connected Transformation is a signature pattern. One object becomes another while preserving source, direction, relationship, and continuity. Implementations should use native shared-element/view-transition mechanisms when safe and provide state-preserving fallbacks when unavailable.

## 26. Haptics

Visual and tactile physics should be synchronized where the target platform supports haptics:

- Tap — tiny pulse
- Toggle — snap
- Selection — tick
- Drag threshold — notch
- Drop — cushioned bump
- Error — restrained double pulse
- Success — soft confirmation

No essential meaning may depend on haptics.

## 27. Intelligent interfaces

Intelligence uses normal Glaze component grammar rather than obligatory glowing gradients.

- **Ambient Intelligence:** small indicators integrated into existing controls.
- **Assisted Intelligence:** contextual Glaze surface connected to the edited/analyzed object.
- **Conversational Intelligence:** larger workspace combining conversation and interactive results.
- **Agentic Intelligence:** persistent activity represented through a Live Surface.

This section governs presentation only. It does not create agent, model, memory, security, privacy, execution, or truth authority.

## 28. Live Surfaces

A Live Surface represents an ongoing process such as upload, navigation, timer, delivery, generation, recording, call, media playback, download, synchronization, or transfer. The same activity may move among notification, Navigation Capsule, lock screen, and desktop task area while remaining recognizably one object.

## 29. Foldables

Folds, hinges, half-open postures, cover displays, dual-pane workflows, orientation changes, and display continuity are first-class constraints. Sheets and content must not blindly span a physical hinge when a pane-aware composition is more usable.

## 30. Desktop Glaze

Desktop is denser than mobile and must not enlarge phone components. It adds tighter spacing/radii where appropriate, persistent navigation, shortcuts, pointer hover, context menus, resizable panels, inspectors, and multi-window workflows while retaining Glaze Material, concentric geometry, connected transformation, iconography, color semantics, and motion principles.

## 31. Accessibility

Accessibility changes rendering, not just preference labels:

- Reduced Transparency increases opacity.
- Increased Contrast strengthens boundaries, text contrast, and layer separation.
- Reduced Motion simplifies morphing into shorter fades/restrained position changes.
- Large Text reorganizes instead of clipping.
- Color Independence prohibits hue-only state communication.
- Show Boundaries adds explicit interactive outlines.
- Touch Assistance enlarges effective hit areas independently of visible size.

The system must remain usable with transparency, blur, complex animation, shaders, or GPU effects disabled.

## 32. Personalization

Three levels are normative:

- **Appearance:** Light, Dark, Deep Dark.
- **Color:** manual Accent Seed or an approved local derivation from environmental/personal imagery.
- **Expression:** Calm, Balanced, Expressive.

Calm reduces motion, color, and shape variation; Balanced is the standard experience; Expressive permits richer transformation, typography, and responsive surfaces without weakening usability.

## 33. Visual signature

A recognizably Glaze interface combines large calm content areas, floating Glaze control islands, ergonomic control placement, concentric geometry, disciplined dynamic color, hierarchy-driven typography, morphing/spring interaction, minimal hard separators, interaction-signaling depth, and layouts that transform rather than resize.

## 34. Avoided practices

Glaze UI rejects: glass everywhere; giant radius everywhere; intelligence gradients as shorthand; meaningless animation; endless nested cards; tiny desktop controls; unreadable transparency; uncontrolled accent use; effects required for usability; and motion that obscures spatial relationships.

## 35. Component families

Normative families:

- Foundations — Color, Typography, Spacing, Shape, Material, Elevation, Grid, Iconography
- Actions — Button, Icon Button, Floating Action Control, Split Button, Button Group
- Inputs — Text Field, Search Field, Slider, Toggle, Checkbox, Radio Control, Picker
- Navigation — Navigation Capsule, Navigation Rail, Sidebar, Breadcrumbs, Tabs
- Containers — Surface, Card, Glaze Panel, Sheet, Dialog, Popover
- Communication — Toast, Banner, Notification, Badge, Tooltip
- Live — Live Surface, Progress Surface, Media Controller, Activity Chip
- Selection — Chip, Segmented Control, Selection Bar
- Data — List, Table, Chart, Timeline, Metric Surface
- Intelligence — Prompt Field, Assist Surface, Generation State, Source Surface, Agent Activity
- Spatial — Floating Toolbar, Control Volume, Environmental Panel, Anchored Surface

## 36. Design tokens

Implementation must expose semantic namespaces equivalent to:

`glaze.color.*`, `glaze.type.*`, `glaze.space.*`, `glaze.shape.*`, `glaze.material.*`, `glaze.motion.*`, `glaze.depth.*`, `glaze.opacity.*`, `glaze.blur.*`, `glaze.border.*`, `glaze.haptic.*`, `glaze.layout.*`, `glaze.state.*`.

Core web Candidate aliases include:

```css
--glaze-shape-control: 999px;
--glaze-shape-card: 24px;
--glaze-space-xs: 4px;
--glaze-space-sm: 8px;
--glaze-space-md: 16px;
--glaze-space-lg: 24px;
--glaze-space-xl: 32px;
--glaze-motion-fast: 140ms;
--glaze-motion-standard: 280ms;
--glaze-motion-expressive: 520ms;
--glaze-touch-min: 48px;
```

Material semantic roles are `material.glaze.soft`, `material.glaze.standard`, `material.glaze.deep`, and `material.glaze.live`. Rendering environments determine exact optical implementation while preserving semantics and fallbacks.

## 37. Governing summary

**Make interaction feel tangible.** Content remains clear and stable. Controls feel soft, dimensional, responsive, and spatially connected. Actions emerge from where they belong. Hierarchy is communicated through shape, scale, color, motion, and depth. Interfaces reshape around the person, device, content, environment, and task.

Until 2.0.0 is promoted, the Candidate artifacts in this branch/release line are implementation and migration work, not Stable production evidence.