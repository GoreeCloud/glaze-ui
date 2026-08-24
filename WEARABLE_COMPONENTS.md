# Glaze UI Wearable Component Candidate Mappings

Status: **Development Candidate**

Current Stable remains: **Glaze UI 1.4.0**

These mappings specialize the Stable Glaze UI component semantics for smartwatch and wearable use. They are candidate-only and do not alter the Stable component contract in `COMPONENTS.md`.

## Wearable action

A wearable action is the primary direct-action primitive.

- Minimum Wear OS interactive target: 48 × 48 dp.
- Prefer one dominant primary action in the immediately visible task region.
- Labels should be short and remain accessible at large text sizes.
- Icon-only actions require an accessible name and a target larger than the visible glyph.
- Primary, secondary, destructive, disabled, loading, pressed, and focused states map to the corresponding Glaze UI semantics.
- Destructive meaning must be expressed in text or accessible naming, not color alone.
- Press motion must remain bounded and must disappear in reduced-motion mode.

## Wearable list item

A wearable list item is the default repeated navigation and selection primitive.

- Use vertically ordered lists as the default information-flow pattern.
- Each directly actionable row must expose a platform-appropriate target and accessible name.
- Keep leading/trailing metadata concise so the center content remains readable on round displays.
- Avoid multiple small adjacent actions inside one row; use progressive disclosure when more than one secondary action is necessary.
- Selection/focus must remain visible for crown, bezel, keyboard, switch, or other non-touch input where supported.

## Wearable status card

A wearable status card presents one bounded status, value, or task context.

- Prefer Solid or Raised presentation.
- Functional Glass may be used only when it improves hierarchy and a solid fallback is guaranteed.
- Keep one dominant value/status and no more than one immediate primary action.
- Do not use card grids that require prolonged scanning.
- Security, privacy, resilience, backup, or recovery states must remain evidence-backed and task-relevant.

## Wearable progress

Progress presentation must distinguish determinate progress from indeterminate activity.

- Use native progress semantics whenever available.
- A determinate value requires an accessible name and value relationship.
- Ambient or always-on presentation must not imply continuous refresh when update cadence is reduced.
- Loading presentation must not remove task context or make destructive controls appear available.

## Wearable toggle and selection

- Prefer platform-native switch, checkbox, radio, picker, and selection controls when they satisfy the task.
- A switch represents an immediate binary setting, not a generic action.
- Selected/checked state must be programmatically exposed.
- Rotary/crown input may adjust bounded selection values, but touch or another native equivalent must remain available unless the platform defines otherwise.

## Wearable navigation

- Prefer platform-native back/dismiss behavior.
- Keep routine navigation shallow.
- Avoid phone-style drawers and hamburger menus.
- Vertical scrolling is the default content navigation model.
- Complications, tiles, widgets, and similar host surfaces should deep-link into a focused task rather than a generic landing page when supported.

## Wearable glance surface

A glance surface is a constrained host-managed surface such as a complication, tile, widget, or always-on presentation.

- Show only the most important current value, state, progress, or action.
- Respect host refresh, privacy, battery, layout, and interaction constraints.
- Do not reproduce the full application UI.
- Present stale or delayed data truthfully.
- Sensitive data must respect platform privacy/redaction behavior.

## Shape and material mapping

- Compact and Standard shapes are the default wearable geometry roles.
- Expressive geometry is reserved for one high-emphasis action or product-defining moment.
- Hero shapes should be rare on a watch and must not crowd task content.
- Clear Glass is not a default wearable material and must not reduce legibility.
- Reduced-transparency behavior must resolve to readable Solid/Raised presentation.

## Typography

- Preserve platform text scaling and accessibility sizing.
- Keep headings and hero text concise enough to reflow without forcing horizontal scrolling.
- Numeric/status values may receive stronger emphasis, but supporting labels remain visible and understandable.
- Truncation must not hide the meaning of critical status or destructive actions.

## Candidate acceptance

These component mappings are not Stable until representative native implementations demonstrate:

- compact round and rectangular layouts;
- 48 dp Wear OS target behavior where applicable;
- touch-only completion;
- rotary/crown-enhanced completion where supported;
- large text and screen-reader semantics;
- reduced motion and reduced transparency;
- non-touch focus visibility;
- interruption/restoration behavior;
- native platform rendering;
- real-device validation.
