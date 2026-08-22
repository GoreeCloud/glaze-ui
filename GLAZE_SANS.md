# Glaze Sans — Future Design Reference

**Status:** Future reference only — no active font-development project, implementation commitment, Candidate release, or Stable requirement.

Glaze Sans is the reserved name for a possible future first-party typeface associated with Glaze UI. The custom-font implementation project is currently scrapped. This document preserves the desired visual and technical direction so a future redesign can begin from an intentional brief instead of the rejected experimental work.

Glaze UI continues to use system/platform-native fonts by default, or approved locally bundled existing open-source fonts when a product has a justified need. No GoreeCloud application should depend on Glaze Sans unless a future project is explicitly restarted, validated, and promoted through the normal Glaze UI lifecycle.

## Visual character

Glaze Sans should feel **beautiful, modern, polished, friendly, calm, and distinctly GoreeCloud**. It should complement Glaze UI's softened geometry and layered surfaces without becoming a novelty font.

The intended character is a **geometric-humanist sans serif with subtle rounding**. Geometry should provide cleanliness and consistency; humanist construction should preserve warmth, familiar reading patterns, and excellent legibility.

Rounded character should appear mainly through carefully softened terminals, curves, joins, counters, and transitions. The design must avoid exaggerated bubble forms, toy-like proportions, excessive softness, handwriting-like construction, or stylistic shapes that make ordinary Latin text look unfamiliar.

## Legibility first

Ordinary English and Latin text must be immediately recognizable before stylistic distinctiveness is considered. Glaze Sans should preserve:

- Familiar alphabet construction and conventional word shapes.
- Comfortable x-height and clear counters.
- Balanced spacing and predictable rhythm.
- Strong differentiation among similar characters.
- Clear rendering at normal interface sizes.
- Readable punctuation, numerals, symbols, and interface text.

The design must make characters such as `I`, `l`, `1`, `O`, `0`, `rn`, and `m` easy to distinguish where practical. Rounded styling must never override readability or accessibility.

## GoreeCloud character

Glaze Sans should be recognizable as its own design without becoming visually strange. Signature character may be introduced through selected glyphs such as `G`, `a`, `g`, `R`, `Q`, `1`, `0`, and `&`, along with terminals, curves, proportions, punctuation, and numeral treatment.

Distinctive details must remain restrained enough that a user notices polish and personality before noticing unusual letter construction. The goal is not to invent a new alphabet; the goal is to give familiar typography a GoreeCloud character.

The typeface must be an original design rather than a tracing, clone, or near-copy of a proprietary vendor typeface.

## Text and display roles

A future family should support both practical interface typography and expressive Glaze UI presentation.

**Text-oriented roles** should prioritize long-session readability for application bodies, settings, navigation, forms, tables, search, notes, messages, metadata, and productivity workflows.

**Display-oriented roles** may carry slightly stronger personality for hero headings, large titles, branding moments, onboarding, marketing surfaces, and expressive Glaze UI composition, while remaining clearly related to the text design.

If optical sizing or separate Text and Display cuts are used, they should feel like one family rather than two unrelated fonts.

## Weight and variable-font direction

A future Glaze Sans family should provide a practical range equivalent to:

- Light
- Regular
- Medium
- Semibold
- Bold
- ExtraBold

A variable-font implementation is preferred when it improves responsive typography, packaging efficiency, interpolation quality, and cross-platform use without reducing compatibility or rendering quality. Weight should be the primary axis. Additional axes should be added only when they solve a real Glaze UI need.

## Interface completeness

Glaze Sans should be designed as an application typeface, not merely as a display alphabet. Numerals, punctuation, currency symbols, mathematical and common technical symbols, arrows, quotation marks, brackets, diacritics, and other characters required by supported GoreeCloud interfaces must be treated as first-class design work.

Tabular or otherwise highly readable numerals should be considered for tables, dates, times, storage values, network information, monitoring data, and administrative interfaces. Character coverage should expand deliberately according to supported GoreeCloud languages and products rather than through incomplete placeholder glyphs.

## Accessibility and quality gates

Any future candidate must be evaluated in representative real interface copy at body, control, navigation, title, and display sizes. Technical font validity, successful compilation, uniqueness, or complete character mapping is not sufficient for acceptance.

A candidate fails if it is visually awkward, malformed, difficult to read, poorly spaced, materially less polished than the approved system-font fallback, or dependent on unusual letter recognition. Review should include small-size rendering, high-DPI displays, light and dark appearances, zoom/scaling, dense administrative screens, long-form text, and representative Mobile, Tablet, Desktop, and TV usage where applicable.

The rejected procedural Glaze Sans 0.1 alpha is historical evidence of what **not** to do. Its alphabet was insufficiently recognizable and did not meet the desired beauty, polish, spacing, or familiar-letterform standard. Future work must begin from this design brief, not by normalizing or promoting that rejected alpha.

## Privacy, delivery, and licensing

If Glaze Sans is ever implemented, applications must load it locally from GoreeCloud-controlled application or design-system assets. Glaze UI must not require Google Fonts or another third-party runtime font-delivery service.

Before any Stable distribution, the typeface and its editable source must use an approved open-source license compatible with GoreeCloud's open-source requirements. Font source, build instructions, generated binaries, licensing, specimens, validation, and release history should be version-controlled and reproducible.

## Future repository boundary

If the project is restarted, `GoreeCloud/glaze-ui` is the preferred canonical location unless the font becomes complex enough to justify a dedicated repository and independent lifecycle. Applications should continue consuming semantic Glaze UI typography roles rather than hard-coding font files, weights, or sizes independently.

## Current boundary

This document preserves design intent only. It does **not** restart Glaze Sans development, make Glaze Sans Planned, add it to the Stable contract, require font binaries, or authorize application adoption. System/platform-native typography remains the Glaze UI default today.

A future restart requires a new explicit project decision, isolated source work, visual review, accessibility validation, licensing review, platform packaging, representative application acceptance, and normal Glaze UI release governance before any application may depend on Glaze Sans.
