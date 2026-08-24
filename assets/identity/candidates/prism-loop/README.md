# Glaze UI — Prism Loop identity candidate

Status: **Candidate — not canonical**

This directory contains a replacement identity direction for Glaze UI. It exists for explicit visual review before any canonical promotion.

## Concept

**Prism Loop** uses two interlocking translucent panes to represent the Glaze UI system itself: layered surfaces, adaptive composition, continuity across form factors, and controlled translucency. The mark is intentionally abstract rather than a generic lettermark.

The candidate is designed to remain distinct from the GoreeCloud platform logo, application icons, Privacy Shield, Wardveil Security, Everkeep, and other first-party system identities.

## Files

- `glaze-ui-mark.svg` — primary full-color standalone mark.
- `glaze-ui-mark-monochrome.svg` — single-color/currentColor mark for high-contrast, print, masks, and constrained surfaces.
- `glaze-ui-lockup.svg` — horizontal mark + wordmark lockup using the system font stack; no bundled or third-party runtime font dependency.

## Candidate palette

The artwork reuses existing Glaze UI semantic identity colors where possible:

- Cyan: `#06B6D4`
- Accent blue: `#366CF6`
- Secondary violet: `#7C5CFF`
- Light violet: `#A594FF`
- Information blue: `#2463D4`

## Promotion boundary

Do not copy these files into a canonical identity path, publish them as the official Glaze UI identity, replace production favicons/icons, or derive release assets from them until the exact candidate is explicitly approved.

After approval, canonical promotion should include deterministic SVG source, reproducible raster derivatives, light/dark/monochrome validation, small-size checks, favicon/application-icon exports, hash-bound release evidence, and repository validation.

Tracks GoreeCloud/glaze-ui#16.
