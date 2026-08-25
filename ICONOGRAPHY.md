# Glaze UI Iconography Contract

Status: **Glaze UI 1.5 Candidate**. Glaze UI 1.4.0 remains the mandatory Stable production target until 1.5 is promoted.

## Principle

Glaze UI iconography is built around **recognizable identity within a shared visual language**. Application, service, system, functional, semantic, file, device, and status icons share a common grammar without erasing product identity.

## Application icons

Application icons use a shared artboard, optical safe area, keylines, alignment guides, softly continuous rounded geometry, and controlled optical correction. Each icon should communicate one dominant concept and remain recognizable from silhouette at reduced size. Miniature interfaces, text-heavy artwork, photographs, tiny decorative detail, uncontrolled gradients, excessive gloss, extreme perspective, and misleading semantic colors are nonconforming.

Application composition uses three conceptual layers:

1. **Foundation** — material, shape, depth, and identity-color environment.
2. **Identity** — dominant recognizable symbol; always visually primary.
3. **Detail** — restrained highlights, secondary geometry, material interaction, and contextual accents.

Glaze materials may use bounded translucency, diffusion, luminosity, tonal gradients, highlights, recessed or raised structure, and accent glazing. Depth must explain construction rather than exist as decoration.

## Service icons

Service icons are intentionally distinct from launchable application icons. Services use simpler geometry, reduced depth, fewer decorative layers, and more symbolic construction. Infrastructure, synchronization, networking, storage, protection, account/provider, and background-process classes may use recurring structural patterns, but no service class may be distinguishable by color alone.

## Core system components

Foundational operating-system components use enduring silhouettes, restrained materials, neutral foundations, and controlled accent use. Their identity must survive future rendering and material evolutions without dependence on temporary visual trends.

## Functional glyphs

Common actions use the system Glaze glyph library rather than application-specific reinterpretations. Shared glyphs must preserve consistent stroke weight, terminal treatment, corner language, optical sizing, negative space, perspective, and visual density. Established symbols must not be reused for unrelated meanings.

Outlined glyphs generally represent available, inactive, or unselected states. Filled or glazed variants represent selected, active, emphasized, or persistent states. Products may not reverse this relationship without a separately standardized semantic exception.

## Semantic symbols

Success, Information, Warning, Danger, Privacy, Security, Protected, Restricted, Online, Offline, Syncing, Paused, and Unavailable use standardized shapes coordinated with the semantic color architecture. Meaning must never depend on color alone; shape, labeling, placement, and context remain part of the contract.

Privacy Shield is authoritative for privacy truth and Wardveil Security is authoritative for security truth. Glaze UI presents supplied state and must not invent, upgrade, or imply stronger evidence through iconography.

## Badges and overlays

Synchronization, notifications, warnings, errors, offline state, sharing, protection, restrictions, management, updates, and unavailable resources use predefined badge forms and anchors. Badge placement must be deterministic. Excessive stacking is prohibited; when multiple conditions compete, the highest-priority current state wins according to the semantic prominence contract.

## Grid and optical correction

All icon classes use a standardized square coordinate system with optical center, safe area, primary geometry region, maximum visual bounds, corner relationships, stroke alignment, and badge anchors. Mathematical consistency is the foundation, but controlled optical correction is required when identical measurements produce perceptually unbalanced results.

## Optical sizes

Responsive iconography is not simple asset scaling. Glaze UI defines four optical-size roles:

- **presentation** — richest material treatment and secondary structure.
- **standard** — normal application/service representation with restrained detail.
- **compact** — simplified geometry, stronger contrast, reduced internal detail.
- **micro** — purpose-built glyph-like representation emphasizing silhouette and essential meaning.

Each product identity must remain recognizable across all required optical sizes.

## Adaptive color and materials

Application identity color may influence foundations, materials, gradients, highlights, and primary identity symbols, but protected semantic colors remain authoritative. Wallpaper, user accent, contextual content, and application identity may influence decorative portions only. Light, dark, high-contrast, grayscale, reduced-transparency, and forced-colors contexts must retain recognizable identity and semantic meaning.

## Motion

Icon motion is permitted only when it communicates state or progress. Synchronization, transfer progress, connectivity, and selection transitions may animate using Glaze motion semantics. Motion must be bounded, interruptible, and replaceable with a static equivalent when reduced motion is requested. Continuous decorative animation without state meaning is nonconforming.

## Accessibility

Icons must remain understandable without exclusive reliance on color, translucency, animation, depth, or fine detail. Interactive icons require accessible names. Unfamiliar symbols require visible labels or explanatory context where meaning cannot reasonably be inferred. Contrast must remain valid across supported materials, wallpapers, appearance modes, and adaptive-color conditions.

## Third-party applications

Third-party developers receive the same grid, keyline, semantic-token, material, badge-anchor, optical-size, export, accessibility, and validation rules. Glaze UI supplies visual grammar while third-party products retain their own recognizable identity. Standardized framing, masking, adaptive backgrounds, or presentation treatments may be applied when needed for ecosystem coherence, but must not destroy or falsely rebrand the original artwork.

## Candidate promotion boundary

This contract is Candidate work. Stable promotion requires source validation, representative rendered review across optical sizes and appearance modes, accessibility and color-vision checks, platform export verification, compatibility assessment, and documented rollback. No downstream application may claim current production conformance against this Candidate until Glaze UI 1.5 is explicitly promoted.