# Adopting Glaze UI

This guide describes how GoreeCloud applications should consume Glaze UI without unnecessary redesign or loss of product personality.

## 1. Record the target version

Record the Glaze UI version used by the application in its project documentation or source metadata. Stable products should state their conformance status and any approved exceptions.

Glaze UI 1.2.0 remains the Stable baseline while 1.3.0 is an acceptance candidate. Consumers must not claim Stable 1.3 conformance until the canonical 1.3 candidate is explicitly promoted.

## 2. Map semantics before replacing visuals

Start with semantic roles rather than copying literal CSS values. Map the application's existing canvas, surfaces, text, status colors, spacing, radii, focus treatment, motion, breakpoints, form states, selection controls, and feedback patterns to Glaze UI tokens and primitives.

Do not replace a successful product-specific composition merely to make it look like another GoreeCloud application.

## 3. Use the material hierarchy intentionally

- Canvas provides the atmospheric background.
- Solid prioritizes readability and is the normal content default.
- Raised separates important content with restrained elevation.
- Glaze adds selective translucency and depth.
- Overlay is reserved for attention-priority surfaces.
- Functional Glass is primarily for navigation, controls, toolbars, floating actions, and transient chrome.
- Clear Glass is reserved for controls over visually rich media such as photos, video, artwork, or maps.

A screen made entirely of translucent cards is not a Glaze UI requirement. Do not migrate ordinary content to glass solely because 1.3 adds richer material roles.

## 4. Adopt expression by role, not decoration

Map Compact, Standard, Expressive, Hero, and Pressed shape roles according to hierarchy and interaction purpose. Keep repeated utility controls calm. Reserve stronger geometry, hero typography, and expressive spatial motion for important actions, selected containers, product-defining moments, and meaningful transitions.

Use effects motion for color, opacity, border, and glow changes. Use spatial motion for position, geometry, layout, size, navigation, and container transformations. Reduced-motion behavior must remove nonessential scaling, shape morphing, and spatial transformation.

## 5. Adopt controls as semantic units

Treat labels, fields, help/error text, selection controls, switches, segmented controls, progress, and banners as complete behavioral units rather than isolated visual decorations.

Prefer native platform controls when they already provide the required semantics and ergonomics. Apply Glaze UI through tokens, spacing, typography, focus treatment, state feedback, and surrounding composition before replacing proven native accessibility behavior with custom controls.

## 6. Preserve accessibility from the beginning

Adopt visible keyboard focus, practical 44px minimum actionable targets, semantic names and states, persistent field labels, programmatically related error/help text, reduced-motion behavior, reduced-transparency behavior, increased-contrast handling, forced-colors support, and solid translucency fallbacks as part of the first implementation rather than as a later styling pass.

## 7. Adapt navigation, grouping, and reachability by available space

Use the four shared ranges:

- Compact: <= 599px
- Medium: 600–1023px
- Expanded: 1024–1439px
- Wide: >= 1440px

Transform navigation and information density when crossing ranges. Do not simply compress desktop layouts onto smaller screens.

On compact touch layouts, frequent actions may move into a lower visual reachability zone when useful, but document order, keyboard order, reading order, and programmatic relationships must remain intact. Adaptive button groups may give high-emphasis actions more space, but visual allocation must not change action meaning or access to sibling actions.

## 8. Keep appearance preferences local by default

Theme or appearance preferences should remain on the client unless a documented product requirement justifies account-level synchronization. Glaze UI itself does not require analytics, remote fonts, remote icons, or third-party UI runtimes.

## 9. Add an application-level contract test

Each stable application should validate the subset of Glaze UI that it actually implements. Tests should focus on durable contracts—semantic tokens, accessible states, form relationships, selection semantics, material boundaries, expressive roles, fallbacks, and dependency boundaries—rather than fragile screenshots or exact DOM structure unless those are truly required.

## 10. Perform visual acceptance

Before a stable release, manually review representative Compact and Expanded layouts in both light and dark appearances. Confirm that forms, focus, errors, selection controls, progress, banners, overlays, navigation, Functional Glass, Clear Glass where used, expressive geometry, adaptive groups, reachability, and motion remain polished and usable. Confirm that the result still feels layered, spacious, ergonomic, and distinctly GoreeCloud rather than like a copied Samsung, Apple, or Google interface.

## Platform-native clients

Native Android, iOS, Linux, or other platform implementations do not need to reproduce web CSS. They should map the same Glaze UI semantic roles into native components while respecting platform ergonomics and accessibility conventions.
