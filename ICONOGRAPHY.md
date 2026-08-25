# Glaze UI Iconography Contract

Status: **Glaze UI 1.5 Candidate**. Glaze UI 1.4.0 remains the mandatory Stable production target until 1.5 is promoted.

## Governing rule

Glaze UI iconography follows one final rule: **identity remains stable while presentation adapts**. The system exists to give applications, services, system components, functional glyphs, semantic indicators, files, folders, devices, accounts, and related visual identities a shared production grammar without erasing their individual identity.

## Master icon grid

Application and service source artwork uses a normalized 1024 × 1024 master coordinate system. The machine-readable Candidate defines an outer canvas, presentation boundary, optical safe area, primary region, core identity zone, optical center, keylines, and system badge anchors.

The grid is an optical construction system rather than a rigid cage. Circles, diagonals, narrow symbols, and unusual silhouettes may use controlled overshoot when needed to achieve equivalent perceived weight. Visual mass is evaluated in context instead of assuming equal mathematical dimensions produce equal prominence.

## Safe zones and keylines

The defining characteristics of an identity remain within the protected optical safe area and core identity zone. Decorative lighting, gradients, surface diffusion, and other bounded presentation effects may extend farther toward the presentation boundary when doing so does not compromise masking, badges, accessibility outlines, focus treatments, synchronization indicators, or future system presentation changes.

Common circle, square, rounded-rectangle, vertical, horizontal, and freeform keylines provide comparable visual weight across unrelated identities. Optical correction remains required when strict geometric equality appears perceptually unbalanced.

## Corner geometry

Glaze UI favors continuous, carefully constructed curvature for outer application containers and related system surfaces. Internal geometry follows object meaning rather than receiving indiscriminate rounding. Family resemblance comes from proportion, construction, material behavior, optical balance, and shared presentation rules.

## Application icon anatomy

A full application icon may use up to five visual layers in this sequence:

1. **Foundation** — dominant silhouette and identity environment.
2. **Material** — translucency, diffusion, surface depth, tonal variation, or glazing.
3. **Identity** — the primary recognizable symbol and highest-priority visual element.
4. **Detail** — restrained secondary information that improves character without being necessary for recognition.
5. **Light** — controlled highlights, reflections, illumination, and environmental response.

Foundation and Identity are required for the application class. Material, Detail, and Light are optional and must be omitted when they do not provide meaningful value. Additional rendering complexity is never a requirement.

## Visual weight and context review

Icons are evaluated together in Launcher grids, search results, task switching, Settings, notifications, and other representative system surfaces. No icon should appear unintentionally enormous, tiny, excessively bright, excessively dark, or disproportionately detailed relative to its neighbors.

## Depth and lighting

Depth explains structure. Raised foreground symbols, recessed objects, and overlapping translucent materials may establish physical or optical relationships, but arbitrary extrusion and decorative three-dimensional effects are nonconforming.

Lighting follows a soft, broad, material-aware environment. Highlights reveal curvature, translucency, layering, or surface structure. Shadows establish separation only where needed. Harsh spotlights, heavy drop shadows, excessive bloom, and artificial plastic gloss are prohibited by the Candidate contract.

## Glaze material families

The reusable icon material roles are:

- **Clear Glaze** — controlled translucency and environmental interaction.
- **Soft Glaze** — greater diffusion and a quieter frosted appearance.
- **Dense Glaze** — stronger opacity with retained depth and luminosity.
- **Tinted Glaze** — application identity color introduced into the material.
- **Luminous Glaze** — restrained internal illumination for appropriate identities and active states.
- **Solid** — maximum clarity for small-scale, high-contrast, or reduced-transparency contexts.

These are semantic material roles rather than immutable texture files.

## Color roles and adaptive color

Icons consume semantic roles rather than arbitrary literal pigments. The Candidate defines identity roles for primary, secondary, surface, highlight, glaze, and foreground treatment together with protected semantic and state roles.

Light mode, dark mode, high contrast, wallpaper context, accent preferences, accessibility configuration, and display behavior may influence bounded portions of presentation. Dark mode is never implemented as simple inversion. Materials, highlights, shadows, surface luminosity, and selected tones may adapt independently while identity geometry and recognizable color relationships remain stable.

Application identity color may influence foundations, materials, gradients, highlights, and primary symbols, but protected semantic meaning remains authoritative. Privacy Shield is authoritative for privacy truth and Wardveil Security is authoritative for security truth. Glaze UI presents supplied state and must not invent, upgrade, or imply stronger evidence through iconography.

## Identity lock

Every important application and service identity requires an identity lock. The lock records the characteristics that must survive every adaptive presentation, which may include the primary silhouette, central symbol, characteristic geometry, dominant color relationship, or another uniquely recognizable property.

Glaze UI may evolve rendering around the identity lock, but it may not adapt an icon so aggressively that users must relearn the identity.

## Service icons

Service icons use a reduced hierarchy:

**Foundation → Capability Symbol → State**

Services use simpler geometry, reduced material depth, fewer decorative layers, and more symbolic construction than ordinary launchable application icons. The `launchable: false` token describes the visual category rather than imposing runtime architecture. A capability that becomes a normal launchable destination must adopt an appropriate launchable identity instead of visually masquerading as a background service.

## Core system components

Foundational operating-system components use enduring silhouettes, restrained materials, neutral foundations, and durable underlying geometry. Rendering techniques may evolve while the recognizable system form remains stable across Glaze UI generations.

## Functional glyph grid and stroke system

Functional glyphs use a separate standardized grid with shared baseline relationships, visual centers, stroke families, terminal styles, corner characteristics, and negative-space principles. Common actions use the system Glaze glyph registry rather than application-specific reinterpretations.

The stroke system uses a limited family of weights. Smaller glyphs may require proportionally stronger strokes while larger glyphs may use more refined geometry. Outlined-to-filled transitions must preserve perceived size and visual weight so state changes do not cause the interface to appear to jump.

Compact, Standard, Large, and Display glyph optical sizes are separate authored representations rather than arbitrary scaling.

## Filled states

Outlined glyphs generally represent available, inactive, or unselected states. Filled or glazed variants represent selection, activation, emphasis, or persistent active state. A filled icon does not automatically mean “more important,” and products may not reverse the established interaction relationship without a separately standardized semantic exception.

## Semantic symbols

Success, Information, Warning, Danger, Privacy, Security, Protected, Restricted, Online, Offline, Syncing, Paused, and Unavailable use standardized system symbols coordinated with semantic color roles. Meaning must never depend on color alone; shape, labeling, placement, and context remain part of the contract.

## Badge anchors and compound states

Notification counts use the upper trailing anchor where appropriate. Ordinary status uses the lower trailing anchor. Security and management indicators use dedicated system-defined positions.

Compact presentation exposes at most one visible priority badge. Priority is determined first by semantic severity and then by contextual importance. Critical security state outranks synchronization, and ordinary notifications must not obscure an error condition. When multiple states genuinely need simultaneous representation, Glaze UI uses a standardized compound-state or expanded labeled treatment rather than stacking several independent badges.

## Optical sizes

Responsive iconography is not simple asset scaling. Glaze UI defines four application/service optical roles:

- **Display** — rich large-scale presentation artwork.
- **Standard** — normal application and service representation with restrained detail.
- **Compact** — simplified geometry, stronger contrast, and reduced internal detail.
- **Micro** — purpose-built essential identity geometry optimized for very small presentation.

As size decreases, secondary detail, weak contrast, thin lines, tiny gaps, subtle material effects, and unnecessary depth are progressively removed. Recognition always takes priority over fidelity to the largest source artwork.

## Monochrome, high-contrast, and reduced-transparency representation

Every important application and service requires a recognizable monochrome representation. Monochrome treatment preserves identity rather than merely converting the full-color icon to grayscale.

High-contrast presentation is purpose-built. Translucent layers may become opaque, low-contrast details may disappear, borders may strengthen, and gradients may simplify while hierarchy and identity remain intact.

When reduced transparency is requested, Glaze materials are replaced with opaque or near-opaque equivalents. Layer relationships remain visible through geometry, borders, luminosity, and tonal separation rather than background diffusion.

## Motion and icon-state transitions

Icon motion extends state rather than forming an independent decorative system. Supported conceptual states include idle, active, progressing, completing, warning, and error.

Transitions should preserve object continuity where possible: synchronization can rotate or reorganize, transfer indicators can resolve naturally into completion, and lock states can transform structurally. Arbitrary fades between unrelated symbols are discouraged where a meaningful geometric transition is possible.

Continuous animation is reserved for cases where continuous activity itself communicates useful information. Motion is interruptible, reduced-motion alternatives are static, and animations normally return to a stable state.

## File, folder, and document icons

Files and documents use a standardized document foundation plus an appropriate format, application, content-type, or semantic indicator. Folder identities use their own container family and may use restrained contextual color without becoming confused with application identities. Real content thumbnails may replace generic symbols when previewing actual content provides greater value.

## Device icons

Phones, tablets, computers, displays, servers, routers, storage devices, wearables, and related hardware use simplified recognizable silhouettes rather than photorealistic hardware rendering. Perspective, stroke, depth, and material treatment remain consistent. Online, offline, trusted, syncing, unavailable, and similar states remain separate semantic layers.

## Security and privacy symbols

Protection, encryption, authentication, identity verification, permissions, restricted access, privacy boundaries, secure connections, compromised states, and critical warnings use established Glaze UI system symbols when the concept already exists. Application-specific replacement symbolism must not fragment high-value security or privacy meaning.

## Validation and quality levels

Important icons are reviewed in light and dark appearance, on neutral and complex backgrounds, in grayscale, high contrast, reduced transparency, neighboring grids, and with system badges applied. Validation covers silhouette recognition, semantic ambiguity, visual weight, material consistency, accessibility, family resemblance, and technical asset integrity.

Quality is evaluated across four required axes: **recognition, consistency, adaptability, and craftsmanship**. Attractive large artwork does not compensate for poor small-size recognition, accessibility, or semantic behavior.

## Glaze UI Native Icon certification

A future **Glaze UI Native Icon** certification process is Planned. Certification is intended to combine automated and visual checks for safe-area compliance, contrast, optical-size support, badge clearance, monochrome compatibility, accessibility behavior, semantic-color usage, required resolutions, and technical asset integrity.

Certification does not mean all icons look alike. It means certified icons respect the same visual and behavioral architecture. No current icon is certified merely because this Candidate contract exists.

## Design tokens

The Candidate exposes semantic concepts such as `icon.size.micro`, `icon.size.compact`, `icon.size.standard`, `icon.size.display`, `icon.stroke.standard`, `icon.corner.continuous`, `icon.material.softGlaze`, `icon.material.denseGlaze`, `icon.identity.primary`, `icon.state.selected`, `icon.state.disabled`, `icon.badge.notification`, `icon.badge.semantic`, and `icon.motion.transition`.

Applications consume semantic contracts rather than reproducing system rules manually.

## Icon Studio

A future Icon Studio or equivalent developer tool is Planned. Its intended responsibilities include master-grid and keyline display, safe-area and optical-boundary overlays, badge exclusion zones, material previews, optical-size generation, light/dark previews, accessibility simulation, contrast inspection, fine-geometry detection, Launcher-grid previews, badge testing, and production export.

Icon Studio is not currently a Stable capability and its Planned status must not be represented as implemented tooling.

## System Icon Registry

A future central registry for standard Glaze UI glyphs and semantic symbols is Planned. The registry is intended to support search by concept, action, object, or semantic role and prevent repeated reimplementation of common concepts such as Share, Search, Delete, Security, Privacy, Sync, Warning, Cloud, Device, Folder, Account, Network, and Settings.

The registry is not currently a Stable capability and must not be represented as complete until implemented and validated.

## Third-party applications

Third-party developers receive the same grid, keyline, semantic-token, material, badge-anchor, optical-size, export, accessibility, and validation rules. Glaze UI supplies visual grammar while third-party products retain their own recognizable identity. Standardized framing, masking, adaptive backgrounds, or presentation treatments may be applied when needed for ecosystem coherence, but must not destroy or falsely rebrand the original artwork.

## Long-term evolution

Icon identity is separated from rendering so future Glaze UI releases can improve materials, lighting, adaptive color, depth, motion, and environmental interaction without forcing unnecessary identity redesign. Geometry that makes an application recognizable should remain comparatively stable while presentation quality evolves around it.

## Candidate promotion boundary

This contract is Candidate work. Stable promotion requires exact-final-revision source validation, representative rendered review across all required optical sizes and appearance modes, accessibility and color-vision checks, platform export verification, compatibility assessment, rollback evidence, and confirmation that Planned certification/tooling/registry capabilities are not falsely represented as Stable implementation.

No downstream application may claim current production conformance against this Candidate until Glaze UI 1.5 is explicitly promoted.
