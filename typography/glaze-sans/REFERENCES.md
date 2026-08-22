# Glaze Sans Reference Research

Status: Research reference — not source adoption

Glaze Sans may study strong open-source interface typefaces to understand proportion, spacing, variable-font engineering, glyph coverage, and QA practices. These references are not Glaze Sans and are not approved source foundations merely because they appear in this record.

## Manrope

Reference role: modern grotesque structure, smooth corners, variable-weight engineering, and restrained UI personality.

Verified source: https://github.com/google/fonts/tree/main/ofl/manrope

Verified license: SIL Open Font License 1.1.

Useful design observation: Manrope's published font log records repeated glyph and kerning refinement, smooth-corner work, and variable-font development. That iterative approach is relevant to Glaze Sans even if Manrope is never used as source material.

## Sora

Reference role: large x-height, generous counters, strong interface legibility, and neutral-but-distinctive digital typography.

Verified source: https://github.com/sora-xor/sora-font

Verified license: SIL Open Font License 1.1.

Useful design observation: Sora is explicitly optimized for interface use and demonstrates how a typeface can retain recognizable text while still carrying a distinct digital personality.

## Onest

Reference role: broad language coverage, alternate glyph engineering, variable weights, reproducible builds, and automated font QA.

Verified source: https://github.com/simpals/onest

Verified license: SIL Open Font License 1.1.

Useful engineering observation: Onest publishes editable source, automated builds, and font QA. Glaze Sans should adopt comparable reproducibility and validation discipline regardless of its eventual outline source.

## Research boundary

No reference font listed here is approved for silent renaming or direct production adoption as Glaze Sans. If an external family becomes an engineering scaffold, the repository must record the exact upstream source revision, license, copyright notices, modifications, renamed family identity, build process, and remaining authored-design work.

The preferred end state is a visually distinct GoreeCloud-controlled family whose provenance is fully transparent and whose runtime delivery remains local/self-hosted.