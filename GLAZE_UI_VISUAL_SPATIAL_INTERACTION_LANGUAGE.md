# Glaze UI — Visual, Spatial, and Interaction Language

**Document status:** Development foundation  
**Stable baseline:** GLAZE UI V1.5.1 / `1.5.1`  
**Consumer eligible:** No  
**Authority:** Presentation-only; this document does not grant operational authority, consent, permission, deployment status, release status, or downstream conformance.

## Overview

Glaze UI is the unified visual, spatial, interaction, component, accessibility, and experience language for the GoreeCloud ecosystem. It defines not only appearance, but how GoreeCloud interfaces move, respond, communicate hierarchy, present information, adapt to devices and inputs, preserve accessibility, and maintain a coherent ecosystem identity.

The language is intended for applications, system interfaces, websites, dashboards, mobile interfaces, desktop environments, television experiences, embedded surfaces, administrative tools, and future GoreeCloud form factors. The goal is for every experience to feel polished, recognizable, expressive, accessible, modern, and cohesive while still allowing individual products to establish their own character.

This Development foundation extends the current `1.5.1` Stable design system without changing `VERSION`, `registry/lifecycle.json`, Stable acceptance evidence, current consumer eligibility, or published Stable entrypoints. Promotion into any future Release Candidate or Stable version requires the separately governed lifecycle and exact-revision qualification process.

## 1. Visual Language

Defines how information, controls, surfaces, and identity are represented. Color is semantic infrastructure: use shared primary, secondary, accent, neutral, surface, background, foreground, semantic, success, warning, error, informational, destructive, disabled, selection, focus, application, user-selectable, light, dark, high-contrast, adaptive, gradient, tonal, harmonized, context-sensitive, category, account, workspace, application, notification, and status color roles. Color must communicate meaning, hierarchy, grouping, and state rather than decoration alone.

## 2. Typography

Defines display, page-title, section-title, heading, subheading, body, label, caption, metadata, button, navigation, numerical, monospaced technical, compact, large-screen, and accessibility text roles. Typography tokens govern size, weight, line height, letter spacing, paragraph spacing, maximum text width, alignment, truncation, scaling, emphasis, and hierarchy, and adapt to screen size, density, accessibility text scaling, interface density, and input method.

## 3. Iconography

Maintains one GoreeCloud icon language with consistent stroke thickness, optical weight, corner treatment, grid alignment, perspective, proportions, padding, balance, fill, and animation behavior. The system supports outline, filled, active, selected, symbolic, status, application, system, navigation, file-type, device, service, and notification icons. Icons must remain understandable without color alone, and common icons keep consistent meaning.

## 4. Shape Language

Defines shared radii and shape semantics for rounded rectangles, pills, circles, cards, sheets, panels, dialogs, containers, navigation surfaces, floating elements, and selection indicators. Shape communicates function: tighter controls, medium card rounding, larger floating-surface rounding, pills for compact categorical/action semantics, and circles for avatars, indicators, or highly focused actions. Arbitrary corner values are prohibited where tokens exist.

## 5. Materials and Surfaces

Treats surfaces as materials with depth and environmental awareness. Supported treatments include transparency, translucency, blur, frost, semi-transparent panels, tinted glass, opaque and layered surfaces, elevated panels, dimmed backgrounds, scrims, overlays, reflective highlights, subtle gradients, edge lighting, and surface tinting. Readability has precedence; opacity rises and blur/transparency reduce when accessibility or performance requires it.

## 6. Elevation and Depth

Uses shadow, surface separation, blur, overlap, border highlights, tonal difference, scale, motion, parallax, light interaction, and contrast to express hierarchy. The governed hierarchy is background, base surface, content container, raised control, floating panel, menu or popover, dialog, and critical system overlay. Depth stays restrained enough to avoid visual clutter.

## 7. Imagery

Defines aspect ratios, cropping, corner rounding, masks, background treatment, overlay gradients, text placement, thumbnail sizing, hero imagery, placeholders, loading behavior, error states, and low-resolution preview behavior so photographs, thumbnails, artwork, previews, and media integrate naturally with Glaze surfaces.

## 8. Illustration and Artwork

Defines compatible proportions, palettes, lighting, geometry, visual weight, and Glaze surface effects for onboarding, empty states, setup, errors, feature introductions, tutorials, documentation, system status, and application artwork.

## 9. Brand Identity

Defines the ecosystem treatment of GoreeCloud logos, application icons, product artwork, system marks, service symbols, startup visuals, splash/loading screens, account identity, and visual motifs. Branding remains recognizable without overwhelming application content.

## 10. Spatial Language

Defines where elements appear and how they relate. Responsive grids cover phones, tablets, foldables, desktop applications, web interfaces, televisions, large displays, and embedded displays. Column count and column size adapt to available space instead of being fixed per product.

## 11. Spacing System

Uses standardized tokens for extra-small, small, medium, large, extra-large, section spacing, page margins, container padding, component padding, and inline spacing. Applications do not invent arbitrary spacing where shared tokens exist.

## 12. Density

Supports comfortable, standard, and compact density. Density may change padding, row height, toolbar height, icon spacing, list spacing, table spacing, and control size while preserving touch-friendly targets whenever touch input is expected.

## 13. Responsive Layouts

Layouts rearrange rather than merely shrink. Glaze supports single-column, two-column, multi-column, sidebar, navigation rail, bottom navigation, top navigation, split view, inspector, and multi-pane compositions. Larger screens use additional space productively while preserving task continuity.

## 14. Component Language

Provides standardized reusable components including buttons, icon buttons, cards, lists, tables, menus, context menus, dialogs, alerts, sheets, popovers, tooltips, tabs, navigation bars, navigation rails, sidebars, toolbars, search bars, text fields, checkboxes, radio controls, toggles, sliders, progress indicators, loading indicators, badges, chips, tags, avatars, breadcrumbs, pagination, date selectors, time selectors, file pickers, color selectors, and command palettes. Components share states, spacing, motion, typography, and accessibility behavior.

## 15. Interaction Language

Every interactive component exposes understandable default, hovered, focused, pressed, selected, active, dragged, disabled, loading, success, warning, and error states. State changes are perceivable immediately and never depend on color alone.

## 16. Motion System

Motion explains object relationships and state changes across page/navigation transitions, panels, cards, sections, reordering, drag/drop, selection, loading, refresh, progress, notifications, confirmations, and icon morphing. Motion is responsive, smooth, physically coherent, and never decoration-only.

## 17. Motion Tokens

Defines instant feedback, fast, standard, emphasized, and long motion tokens plus shared easing curves, spring behavior, acceleration, deceleration, fade timing, scale timing, and slide timing. Products do not create unrelated timings when a shared semantic token applies.

## 18. Reduced Motion

Reduced-motion mode replaces nonessential complex movement with fades, crossfades, immediate state changes, reduced scaling, and reduced parallax. Essential information never depends exclusively on animation.

## 19. Gestures

Defines consistent tap, double tap, long press, swipe, drag, drop, pinch, zoom, rotate, edge swipe, pull-to-refresh, swipe action, and drag-selection semantics. A gesture should not perform dramatically different actions across products without a contextual reason.

## 20. Haptics

Defines subtle, optional haptic categories for selection, confirmation, warning, error, toggle, drag threshold, snap, long press, and completion. Devices without haptics remain fully understandable.

## 21. Sound

Defines optional system sound categories for notifications, confirmations, errors, warnings, incoming communication, completed tasks, device connection, and security alerts. Sound may reinforce state but is never required to understand it.

## 22. Feedback and Status

Standardizes loading, progress bars, progress circles, skeletons, toasts, inline messages, success messages, warning banners, error banners, offline indicators, synchronization states, background activity, pending changes, and saved states. Users must be able to determine whether an action succeeded, failed, remains pending, or is unavailable.

## 23. Data Visualization

Defines line, bar, area, pie-style, gauge, progress-ring, heat-map, timeline, histogram, sparkline, table, status-dashboard, and activity-graph patterns. Charts follow shared color, type, spacing, label, tooltip, accessibility, selection, and hover rules; meaningful differences remain perceivable without color alone.

## 24. Content Language

Defines clear, concise, human-readable, consistent, action-oriented language for button labels, navigation labels, errors, empty states, confirmations, settings descriptions, notifications, permissions, warnings, and destructive actions. Unnecessary technical terminology is avoided.

## 25. Accessibility

Accessibility is structural, not a later add-on. Glaze supports high contrast, adjustable typography, screen readers, keyboard navigation, visible focus, switch navigation, voice interaction, reduced motion, reduced transparency, large touch targets, color-independent status, semantic structure, and accessible data visualization. Compatible settings propagate across applications.

## 26. Adaptive Behavior

Adapts presentation to screen size, orientation, window size, input type, pointer availability, touch availability, keyboard availability, device performance, display contrast, accessibility settings, and battery-saving modes while preserving product capabilities and authority boundaries.

## 27. Theming

Provides a shared theming engine controlling palette, accent, surface transparency, blur strength, corner radius, density, type scale, icon treatment, animation intensity, and background appearance. Themes remain constrained by accessibility and usability requirements.

## 28. Application Personalization

Permits products to customize accent colors, artwork, illustrations, application icons, category colors, and specialized components while continuing to share typography hierarchy, core icon language, spacing, motion principles, accessibility behavior, surface behavior, navigation logic, and component architecture.

## 29. Design Tokens

Exposes core design decisions as reusable color, typography, spacing, radius, border, shadow, elevation, opacity, blur, motion, size, icon, and breakpoint tokens so multiple GoreeCloud runtimes can implement the same semantics without copying arbitrary values.

## 30. Glaze UI Design Layers

Organizes Glaze into five layers: Visual Language (appearance), Spatial Language (arrangement), Interaction Language (behavior), Component Language (building blocks), and Experience Standards (ecosystem-wide quality). These layers create a shared architecture without forcing every application into identical compositions.

## 31. Core Glaze UI Principle

Every GoreeCloud interface should feel like a member of the same family without requiring identical appearance. Consistency comes from shared design principles, typography, iconography, color logic, shape language, spacing, materials, motion, components, accessibility, and interaction behavior; product character is layered on top. Glaze UI is therefore the complete visual, spatial, interaction, component, accessibility, and experience language of the GoreeCloud ecosystem.

## Development implementation

This language is implemented in Development by the following repository artifacts:

- `contracts/experience-language.dev.json` — machine-readable semantic contract.
- `schemas/experience-language.schema.json` — structural validation contract.
- `tokens/glaze-experience-language.dev.json` — reference-only token ownership map over existing Glaze token sources.
- `scripts/validate_glaze_experience_language_development.py` — fail-closed source validator.
- `.github/workflows/glaze-experience-language-development.yml` — independent contract and Stable-boundary CI.

The Development token map references existing token authorities instead of duplicating or rewriting their raw values. Existing Stable files remain intact unless a later governed release explicitly promotes a successor.

## Release and evidence boundary

Documentation, machine-readable contracts, and green Development CI establish source-level implementation of this language only. They do **not** by themselves establish human usability acceptance, assistive-technology acceptance, device/runtime acceptance, downstream consumer conformance, tag or GitHub Release publication, deployment, or production acceptance. Any future lifecycle promotion must bind those claims to the exact revision and evidence required by current GoreeCloud governance.
