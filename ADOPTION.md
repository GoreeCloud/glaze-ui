# Adopting Glaze UI

This guide describes how GoreeCloud applications should consume Glaze UI without unnecessary redesign or loss of product personality.

## 1. Record the target version

Record the Glaze UI version used by the application in its project documentation or source metadata. Stable products should state their conformance status and any approved exceptions.

## 2. Map semantics before replacing visuals

Start with semantic roles rather than copying literal CSS values. Map the application's existing canvas, surfaces, text, status colors, spacing, radii, focus treatment, motion, breakpoints, form states, selection controls, and feedback patterns to Glaze UI tokens and primitives.

Do not replace a successful product-specific composition merely to make it look like another GoreeCloud application.

## 3. Use the surface hierarchy intentionally

- Canvas provides the atmospheric background.
- Solid prioritizes readability and resilience.
- Raised separates important content with restrained elevation.
- Glaze adds selective translucency and depth.
- Overlay is reserved for attention-priority surfaces.

A screen made entirely of translucent cards is not a Glaze UI requirement.

## 4. Adopt controls as semantic units

Treat labels, fields, help/error text, selection controls, switches, segmented controls, progress, and banners as complete behavioral units rather than isolated visual decorations.

Prefer native platform controls when they already provide the required semantics and ergonomics. Apply Glaze UI through tokens, spacing, typography, focus treatment, state feedback, and surrounding composition before replacing proven native accessibility behavior with custom controls.

## 5. Preserve accessibility from the beginning

Adopt visible keyboard focus, practical 44px minimum actionable targets, semantic names and states, persistent field labels, programmatically related error/help text, reduced-motion behavior, increased-contrast handling, forced-colors support, and solid translucency fallbacks as part of the first implementation rather than as a later styling pass.

## 6. Adapt navigation by available space

Use the four shared ranges:

- Compact: <= 599px
- Medium: 600–1023px
- Expanded: 1024–1439px
- Wide: >= 1440px

Transform navigation and information density when crossing ranges. Do not simply compress desktop layouts onto smaller screens.

## 7. Keep appearance preferences local by default

Theme or appearance preferences should remain on the client unless a documented product requirement justifies account-level synchronization. Glaze UI itself does not require analytics, remote fonts, remote icons, or third-party UI runtimes.

## 8. Add an application-level contract test

Each stable application should validate the subset of Glaze UI that it actually implements. Tests should focus on durable contracts—semantic tokens, accessible states, form relationships, selection semantics, fallbacks, and dependency boundaries—rather than fragile screenshots or exact DOM structure unless those are truly required.

## 9. Perform visual acceptance

Before a stable release, manually review representative Compact and Expanded layouts in both light and dark appearances. Confirm that forms, focus, errors, selection controls, progress, banners, overlays, and navigation remain polished and usable. Confirm that the result still feels layered, spacious, and distinctly GoreeCloud.

## Platform-native clients

Native Android, iOS, Linux, or other platform implementations do not need to reproduce web CSS. They should map the same Glaze UI semantic roles into native components while respecting platform ergonomics and accessibility conventions.
