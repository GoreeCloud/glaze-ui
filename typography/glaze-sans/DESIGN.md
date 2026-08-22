# Glaze Sans Design Direction

Status: **Experimental — visual direction under review**

Glaze Sans is the planned first-party typeface family for Glaze UI. This document governs the design direction while the typeface remains experimental. It does not make Glaze Sans a Stable Glaze UI dependency and does not authorize downstream application adoption.

## Design objective

Glaze Sans must look like polished, natural English and Latin typography before it expresses a GoreeCloud-specific personality. Distinctiveness must come from proportion, spacing, curves, terminals, selected glyph details, and weight behavior rather than from deforming familiar letters.

The desired visual character is:

- immediately readable;
- soft and subtly rounded;
- warm rather than sterile;
- modern and premium rather than playful or novelty-driven;
- suitable for dense application interfaces and large expressive headings;
- calm in body text and more recognizable in display use;
- consistent with Glaze UI rounded geometry without imitating rounded cards as literal bubble letterforms.

## Rejected first alpha

The original 0.1 alpha is permanently rejected as a design direction. Its pseudo-handwritten/constructed forms made ordinary Latin text unfamiliar, weakened word recognition, and produced inconsistent spacing and texture. It must not be promoted, reused as a fallback, or adopted by a GoreeCloud application.

## Direction 02 reset

The second reset restored conventional Latin structure and professional UI readability. It is retained only as a readability reference. It does not yet provide enough original Glaze personality to be considered an approved typeface design.

## Direction 03 target

The next design round must preserve Direction 02 readability while introducing restrained rounded character.

### Core proportions

- Medium-to-large x-height for application readability.
- Conventional cap-height and ascender/descender relationships.
- Open counters at small sizes.
- Comfortable default spacing with no monospaced or handwritten rhythm.
- No exaggerated circular construction that makes text look childlike or decorative.

### Letterform rules

Text forms must remain conventional. Lowercase `a`, `e`, `g`, `r`, `s`, and `t` receive special readability review because changes to these glyphs strongly affect English word recognition.

Potential GoreeCloud signatures may be developed in `G`, `Q`, `R`, `&`, `1`, and `0`, but every signature must remain instantly recognizable at normal UI sizes.

Rounded terminals should be visible at display sizes yet restrained in body text. Curvature must feel designed into the stroke system rather than added as an afterthought.

### Text and Display behavior

Glaze Sans is planned as one coherent family with two optical intentions:

- **Glaze Sans Text** — conventional, highly legible application typography for labels, navigation, settings, forms, tables, notifications, documentation, and body copy.
- **Glaze Sans Display** — a more expressive treatment for hero text, major headings, marketing surfaces, large empty states, and selected branded moments.

Display may use slightly stronger rounding or alternate details, but it must not become a separate novelty alphabet.

### Weight plan

Initial design review targets:

- Regular 400
- Medium 500
- SemiBold 600
- Bold 700
- ExtraBold 800

Lighter weights, italics, additional OpenType features, optical-size automation, and expanded scripts are later work unless required to resolve a specific acceptance need.

## Mandatory readability gate

A Glaze Sans candidate fails if an ordinary reader has to study the typeface to identify normal English words. In particular:

- `I`, `l`, and `1` must remain distinguishable;
- `O` and `0` must remain distinguishable;
- `rn` must not collapse into `m`;
- `cl` must not collapse into `d`;
- punctuation and numerals must be unambiguous;
- lowercase word shapes must remain conventional;
- rounded details must not close counters or reduce clarity.

A candidate that is technically valid but visually less readable than the Glaze UI system-font fallback cannot pass promotion.

## Privacy and delivery

Glaze Sans must be distributable as a local GoreeCloud-controlled asset. GoreeCloud applications must not require Google Fonts, a third-party font CDN, analytics, telemetry, or any other runtime font service to render the family.

Unsupported scripts must use documented platform/system fallbacks rather than displaying missing-glyph boxes or forcing an incomplete Glaze Sans character set.

## Source strategy

The project may use permissively licensed open-source typefaces as research references or as an explicitly documented engineering scaffold during exploration. Any derivative work must preserve required attribution and license notices and must be renamed where required by the source license.

A reference scaffold is not automatically the final Glaze Sans design. The final family must have sufficient intentional GoreeCloud-authored design work to justify its own identity, and its provenance must remain transparent.

## Promotion boundary

Glaze Sans remains Experimental until all of the following are complete:

1. Human approval of the visual direction.
2. Reproducible editable font sources are committed.
3. License and provenance are verified.
4. Required glyph coverage is defined and validated.
5. Text and display specimens pass visual review.
6. UI-size rendering is tested across supported form factors.
7. Accessibility and confusing-glyph review passes.
8. Web and native packaging are reproducible.
9. Glaze UI semantic typography tokens integrate the approved family with safe fallbacks.
10. Exact candidate CI and rendered/native acceptance evidence pass.

Until then, Stable Glaze UI typography remains the production authority.