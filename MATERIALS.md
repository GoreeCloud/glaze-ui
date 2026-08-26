# Glaze UI Material and Depth Contract

Status: **Glaze UI 1.5 Candidate**

This document defines the semantic material, depth, translucency, elevation, backdrop, and overlay behavior used by GoreeCloud interfaces. It extends the Stable 1.4 visual foundation without changing the current Stable production target.

## Purpose

Material exists to communicate hierarchy, containment, continuity, focus, and interaction state. It is not decoration. Blur, translucency, shadow, glow, and glass treatments must never reduce legibility, hide state, imply security/privacy guarantees, or become a substitute for information architecture.

## Canonical material stack

Glaze UI defines six semantic material roles:

1. **Canvas** — application/page background. It establishes environmental tone and may carry restrained contextual color.
2. **Solid** — default content surface. Use for reading, forms, dense data, long-lived panels, and any content where stable contrast is more important than environmental blending.
3. **Raised** — elevated content surface. Use for cards, inspectors, menus, floating panels, and containers that need clear separation without modal authority.
4. **Functional Glass** — translucent chrome for navigation, toolbars, compact controls, floating utility regions, and transient interface framing. It may sample the backdrop only within bounded regions.
5. **Clear Glass** — specialized low-opacity glass for controls over visually rich media where preserving the media is essential. It is never the default content material.
6. **Overlay** — modal, popover, command, sheet, dialog, or transient high-authority surface above a scrim or equivalent separation mechanism.

Material roles are semantic, not visual presets. Consumers choose the role required by hierarchy and task, then map it to platform-native capabilities while preserving the same meaning.

## Depth model

Depth is expressed through semantic levels rather than arbitrary z-index values:

- `base` — canvas and ordinary in-flow content.
- `raised` — cards and elevated panels.
- `navigation` — persistent application chrome.
- `scrim` — modal separation layer.
- `overlay` — dialogs, popovers, sheets, command surfaces.
- `toast` — transient non-blocking notification layer.

A higher depth level does not automatically authorize stronger blur, opacity, saturation, or color. Those properties remain governed by the material role.

## Material selection rules

- Ordinary content defaults to **Solid** or **Raised**.
- Glass is selective and functional. A page composed primarily of translucent cards is non-conformant unless the product has a documented visual requirement that still preserves readability and performance.
- Functional Glass is appropriate for controls and navigation that benefit from environmental continuity.
- Clear Glass is limited to media-overlay controls and similarly constrained cases.
- Overlay is reserved for transient hierarchy that must appear above the current task.
- Content requiring high reading concentration, long-form text, dense tables, code, legal text, security/privacy explanations, recovery information, or destructive confirmations should prefer Solid/Raised surfaces.

## Backdrop sampling

Backdrop sampling must be local, bounded, and truthful:

- Never sample across unrelated windows or security boundaries.
- Do not imply that content behind a surface is visible or available when the platform cannot provide that backdrop.
- If backdrop filtering is unsupported, disabled, too expensive, or inaccessible, fall back to an opaque or near-opaque semantic surface without changing the component hierarchy.
- Sampling must not make protected semantic colors indistinguishable.
- A material may inherit contextual tone, but it must not inherit semantic meaning from arbitrary background pixels.

## Contrast and legibility

Every material must preserve the contrast and readability requirements defined by Glaze UI accessibility and color contracts.

- Text and functional icons must remain legible over the worst permitted backdrop, not merely a curated demo image.
- When contrast cannot be guaranteed, increase surface opacity, add a local scrim, or fall back to Solid/Raised.
- Blur cannot be used as the only contrast mechanism.
- Critical status, privacy, security, recovery, and destructive-action content may not rely on translucency to remain legible.

## Reduced transparency

Platforms or users may request reduced transparency. Glaze UI treats this as a first-class accessibility preference.

When reduced transparency is active:

- Functional Glass becomes a high-opacity semantic surface.
- Clear Glass becomes a stable opaque/near-opaque media control surface.
- Background blur and saturation effects are removed.
- Hierarchy remains communicated through borders, tonal separation, spacing, and elevation rather than transparency.
- No functionality, affordance, state, or information may disappear.

Reduced transparency is independent from reduced motion. Consumers must support both simultaneously.

## Performance budget

Backdrop effects can be expensive. Consumers must prefer stable interaction performance over visual effects.

- Avoid large continuously updating backdrop-filter regions.
- Avoid stacking multiple blurred translucent surfaces over one another.
- Prefer one bounded glass region over many nested glass descendants.
- Disable or simplify costly effects under platform power-saving, low-performance, remote-display, or constrained-rendering conditions when such signals are available.
- Performance degradation must fall back toward Solid/Raised semantics rather than removing hierarchy.

## Shadows and elevation

Shadow communicates separation, not decoration.

- `soft` — subtle separation for low-elevation cards and panels.
- `raised` — stronger separation for floating content.
- `overlay` — high separation for dialogs, menus, and transient overlays.
- `tvFocused` — focus separation for far-view TV interactions where scale/lift alone is insufficient.

Dark surfaces should use lower-luminance, broader shadows or tonal separation rather than bright halos. Semantic status must never be communicated by shadow color alone.

## Borders and edge definition

Translucent materials should retain a quiet edge treatment when needed to remain visible against variable backgrounds. Borders must use semantic line colors and must not become bright glass rims that overpower content.

## Interaction and motion

Material transitions follow `MOTION.md`:

- Opacity, tint, border, and subtle shadow changes are effect motion.
- Geometry, lift, sheet movement, and spatial hierarchy changes are spatial motion.
- User-driven material transitions remain interruptible.
- Reduced-motion mode removes nonessential geometry travel while preserving state changes.
- Material animation must not continuously shimmer, pulse, refract, or drift without a functional reason.

## Form-factor behavior

### Mobile

Favor stable Solid/Raised reading surfaces with selective glass for bottom navigation, compact toolbars, media controls, and transient sheets.

### Tablet

Use material to distinguish persistent navigation, primary content, contextual panes, and floating utilities without turning every pane into glass.

### Desktop

Use restrained depth for resizable workspaces. Menus, inspectors, toolbars, command palettes, and transient panels may use Functional Glass or Overlay where platform rendering remains performant and legible.

### TV

Favor opaque or near-opaque surfaces and strong focus separation. Distant viewing, content variability, and hardware performance take priority over subtle translucency.

## Authority boundaries

Glaze UI controls presentation only.

- **Privacy Shield** is authoritative for privacy-control state and privacy claims.
- **Wardveil Security** is authoritative for security and protection state.
- **Everkeep** is authoritative for resilience, backup, recovery, preservation, portability, succession, and digital-legacy state.
- **GoreeCloud Mesh** is authoritative for cross-product coordination and governance state.

A glass, glow, depth, color, or overlay treatment must never manufacture or upgrade those states.

## Candidate acceptance

Promotion requires all of the following:

- machine-readable material-role definitions;
- web primitives with reduced-transparency and unsupported-backdrop fallbacks;
- fail-closed source validation;
- exact-revision CI validation;
- representative rendered acceptance across light/dark themes and supported form factors;
- documented contrast and performance review for glass-heavy representative surfaces;
- no regression to current Stable consumer behavior until 1.5 is formally promoted.

Until those gates are satisfied, this contract remains Candidate and Glaze UI 1.4.0 remains the current Stable production baseline.
