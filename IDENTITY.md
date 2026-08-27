# Glaze UI Visual Identity Contract

Status: **Approved canonical artwork**

Canonical identity: **Facet**

Glaze UI 1.5.0 is the current Stable GoreeCloud design-system baseline. Facet is the sole approved Glaze UI logo, icon, and visual identity artwork.

## Approval record

The GoreeCloud administrator explicitly approved Facet as the official Glaze UI identity on 2026-08-27 and directed that alternate Round 4 concepts not remain in the current repository tree.

The exact approved scalable source is:

- Path: `assets/identity/official/facet/glaze-ui-mark.svg`
- SHA-256: `3c9566bf21c5bed4121547c3d5c79c34e4f3e60105179b7f2342c4b60ae91a61`
- Source role: authoritative canonical artwork

The canonical source is the exact reviewed Facet SVG promoted without geometry changes. Public and generated representations must trace back to this source.

## Identity role

Glaze UI is a GoreeCloud platform/design-system identity, not an ordinary Suite application. Facet communicates layered hierarchy, selective translucency, calm structure, adaptive composition, and reusable interface geometry while remaining visually distinct from GoreeCloud platform, product, privacy, and security identities.

## Canonical-use rules

- Use Facet as the Glaze UI mark wherever a Glaze UI logo or icon is required.
- Do not substitute alternate Glaze UI artwork.
- Do not redraw, rotate, stretch, distort, or alter the Facet geometry.
- Full-color derivatives must preserve the approved source geometry and intended gradient relationships.
- Monochrome, favicon, raster, platform, and size-specific derivatives must be reproducibly derived from the canonical source.
- Decorative presentation may adapt to light/dark surfaces, accessibility modes, and supported output formats without changing the underlying identity geometry.
- The SVG must remain self-contained: no scriptable behavior, embedded remote resources, or external runtime dependencies.

## Traceability

`assets/identity/official/facet/glaze-ui-mark.svg` is the only canonical scalable source. Build systems may copy it byte-for-byte or produce deterministic derivatives from it. A derivative that cannot be traced to the approved source must not be represented as official Glaze UI artwork.

## Public-site state

`design.goreecloud.com` uses Facet as the official Glaze UI favicon, header mark, hero identity artwork, identity reference, and footer mark. The public artifact must be built from the canonical repository source rather than a detached copy.

## Future changes

Facet remains canonical until the GoreeCloud administrator explicitly approves a replacement identity. Merely committing, generating, rendering, or proposing alternate artwork does not change canonical status.