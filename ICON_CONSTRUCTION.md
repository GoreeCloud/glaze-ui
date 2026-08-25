# Glaze UI Icon Grid, Geometry, Materials, and Construction Contract

Status: **Glaze UI 1.5 Candidate**. Glaze UI 1.4.0 remains the mandatory Stable production-conformance baseline until 1.5 is explicitly promoted.

## Purpose

This contract is the production-construction layer beneath `ICONOGRAPHY.md`. `ICONOGRAPHY.md` defines the broader visual grammar; this document defines how application and service identity assets are constructed, simplified, packaged, validated, and described for tooling.

## Master canvas and protected zones

Primary application identity source artwork uses a normalized **1024 × 1024** master canvas with optical origin **512 × 512**.

The default construction zones are percentage-based rather than fixed clipping masks:

- **Canvas Boundary** — 100% of the coordinate space.
- **Presentation Zone** — approximately 90% of the canvas. It contains the outer presentation container, permitted large material response, and controlled optical overshoot.
- **Optical Safe Zone** — approximately 76% of the canvas. It contains the majority of important identity geometry.
- **Core Identity Zone** — approximately 60% of the canvas. It contains the characteristics that must remain recognizable at Compact and Micro optical sizes.

Optical correction is permitted when geometry requires it. Mathematical centering is not sufficient when perceptual visual mass is unbalanced.

## Keyline families

The master grid supports circular, continuous-square, vertical, horizontal, compact-object, and freeform keyline families. Keylines are visual-weight references, not mandatory masks.

Circular and pointed geometry may use controlled overshoot when needed to appear equal in scale to rectangular geometry. Diagonal elements may receive similar optical compensation.

## Continuous corner system

Glaze UI construction uses four conceptual curvature levels:

- **Subtle** — technical, document-oriented, or highly structured forms.
- **Standard** — default application-container curvature.
- **Expressive** — creative, entertainment, approachable, or consumer-oriented identities.
- **Full** — circles, capsules, and completely rounded forms.

Curvature should transition continuously between straight edges and curved corners rather than defaulting to unrelated arbitrary quarter-circle radii.

## Container and foundation

An application may use a recognized outer container, a partially broken container, or a transparent/freeform foundation as long as visual mass and the Presentation Zone remain controlled. Family resemblance must not require every application to become the same rounded square with different colors.

The Foundation layer establishes the dominant visual environment. It may be neutral, chromatic, translucent, opaque, luminous, gradient-based, or material-driven, but it must support rather than compete with the identity.

## Material hierarchy

The reusable material vocabulary remains Clear Glaze, Soft Glaze, Dense Glaze, Tinted Glaze, Luminous Glaze, and Solid Material.

When materials overlap, depth order is explicit:

1. Background material provides environmental context.
2. Structural material defines the main form.
3. Identity material defines the recognizable symbol.
4. Highlight material provides controlled optical response.

Multiple equally prominent translucent layers are prohibited because they create visual ambiguity.

## Identity and Identity Lock

The Identity layer is the most important layer. Recognition must survive removal of gradients, translucency, lighting, shadows, and secondary detail.

Every major application and service identity requires an **Identity Lock**. The lock records stable recognition properties such as primary geometry, silhouette, orientation, distinctive negative space, characteristic proportions, and essential color relationships. Presentation may evolve around the lock; the lock itself must not drift casually across themes, sizes, accessibility modes, or redesigns.

## Detail and light

Secondary detail is used only when it improves recognition, structure, or meaningful character. Detail must be progressively removable.

Light is treated as a material response rather than painted decoration. Highlights should follow curvature, translucency, polish, or another physical/material rationale. Internal illumination must correspond to a material or conceptual object capable of supporting it. Visual hierarchy must remain readable when highlights are removed.

## Tonal gradients and environmental response

Gradients establish volume, material, luminosity, atmosphere, or identity. They should remain within coherent tonal relationships unless spectral color is itself essential to the identity.

Adaptive presentation may respond to wallpaper luminosity, system appearance, selection state, accessibility configuration, and system accent configuration. Adaptation may change material density, edge separation, highlight intensity, or related presentation properties, but it must not destabilize recognition.

Light and dark presentations are designed independently. Dark presentation is not a simple inversion of light presentation.

## Negative space and stroke architecture

Negative space is an active identity component. Important internal gaps must remain distinguishable in Compact and should survive in simplified form in Micro.

Outlined identity strokes and functional glyphs use a controlled stroke system. Stroke strength may increase proportionally as presentation size decreases. Micro representations should prefer simplified filled geometry over delicate strokes when that improves reliability.

## Optical representations

Every major application and service identity supports purpose-built optical representations:

- **Display** — full material expression for large promotional and detail surfaces.
- **Standard** — definitive everyday launcher/search/settings representation.
- **Compact** — simplified geometry and stronger contrast for dense lists, menus, navigation, and task surfaces.
- **Micro** — purpose-built symbolic representation retaining primarily the Identity Lock.

The reduction sequence is:

**Material richness → structural clarity → silhouette → identity.**

Scaling Display artwork down is not an acceptable substitute for Compact or Micro construction.

## Application and service family DNA

Related applications may share one or two controlled characteristics such as material behavior, secondary geometry, recurring motif, foundation treatment, or compositional rhythm. They must not share the exact same symbol with only color differences.

Services may use stronger recurring structural motifs because categorical recognition is useful for storage, networking, synchronization, identity, security, indexing, notification, media processing, and related infrastructure families. Service family traits still must not erase individual service recognition.

## Semantic overlays and badges

Identity remains stable when state changes. Success, information, warning, danger, privacy, security, syncing, offline, paused, restricted, managed, unavailable, and related states are communicated through standardized semantic layers rather than recoloring the base identity into a different product.

Notification quantity and semantic condition are separate systems.

Badge geometry uses a secondary grid. Trailing corners are primary badge territories, and indispensable identity information must not be placed underneath those expected territories. Compact presentation remains bounded to the highest-priority visible semantic badge when several states compete.

## Selected, disabled, unavailable, and progress states

Selection normally modifies the surrounding system surface through an accent glaze, halo, tonal shift, focus border, or equivalent contextual treatment rather than dramatically recoloring the identity.

Disabled state reduces saturation, material activity, luminosity, or contrast while preserving recognition. Unavailable is a distinct semantic condition indicating that the underlying resource, service, device, application, or capability cannot currently be reached or provided.

Progress indicators remain separate from identity. Downloads, installations, synchronization, processing, backups, and updates may use rings, tracks, overlays, or adjacent indicators while the primary identity remains visible.

## Motion grammar

Icon motion is classified as **State Transition**, **Progress**, **Activity**, **Attention**, or **Confirmation**. These categories have different timing, repetition, and stopping behavior.

Persistent motion is not used merely because animation is available. Once an animation has communicated its information, it normally stops. Reduced-motion preferences replace unnecessary physical transformations with simpler state changes.

## Monochrome identity and icon/text pairing

Major identities require purpose-built monochrome representations where necessary rather than generic grayscale filtering.

When icons appear next to text, perceived visual centers align to typography rather than only to raw bounding boxes. Small icons may require vertical optical correction.

Typography inside application icons is generally avoided. A letter, numeral, or typographic symbol is permitted only when it is genuinely part of the graphical identity and remains recognizable at every required optical size.

## Validation matrix

Important icons are validated through all of the following contexts:

- color-vision simulation;
- grayscale;
- high/increased contrast;
- reduced transparency;
- reduced motion;
- bright, dark, colorful, detailed, and low-contrast backgrounds;
- Launcher-grid comparison with unrelated Glaze UI identities;
- squint/blur silhouette review;
- Micro representation review;
- standardized badge collision review;
- light and dark appearance;
- monochrome identity review.

An icon that succeeds alone but disrupts the system grid is not complete.

## Structured icon asset package

A production icon is a structured identity asset, not a single bitmap. A complete package may include:

- authoritative vector or high-resolution source;
- Display representation;
- Standard representation;
- Compact representation;
- Micro representation;
- monochrome identity;
- high-contrast behavior;
- reduced-transparency behavior;
- identity colors;
- material metadata;
- Identity Lock metadata;
- badge-clearance metadata;
- adaptive-appearance metadata;
- optional motion definitions.

The operating environment should select the correct representation from the package rather than rely entirely on raster scaling.

## Machine-readable icon manifest

Each package should include a machine-readable manifest conforming to `schemas/icon-manifest.schema.json`. The manifest records identity category, source identity, optical variants, Identity Lock, identity colors, materials, badge clearance, adaptive appearance, accessibility behavior, semantic restrictions, and optional motion capabilities.

`examples/icon-manifest.example.json` is a non-canonical schema example only. It does not certify or approve any current GoreeCloud artwork.

## Planned authoring and linting tooling

**Glaze UI Icon Studio**, live environment preview, automatic production export, icon linting, and the searchable **System Icon Registry** remain **Planned** capabilities. Their intended contract is documented, but no current Stable tooling or certification claim exists merely because machine-readable construction data and schemas are present.

A future linter is expected to detect missing optical variants, invalid dimensions, unsupported color profiles, contrast problems, badge collisions, excessive detail, missing monochrome identity, protected semantic-color misuse, and similar violations. Technical errors and subjective design recommendations should remain distinguishable.

## Future-proof rendering

Source identity is separated from final rendering. Future material systems, HDR, spatial interfaces, richer lighting, depth, environmental reflections, and new display technologies may change presentation without replacing the underlying Identity Lock or semantic structure.

The Glaze UI icon is therefore treated as a **responsive visual identity asset** rather than a static bitmap.

## Candidate boundary

This contract strengthens the isolated Glaze UI 1.5 Candidate. It does not certify existing artwork, approve new canonical identities, make Icon Studio or the registry Stable, migrate downstream applications, or change Glaze UI 1.4.0 Stable production requirements.