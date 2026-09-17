# GLAZE UI Token Authority

`VERSION` and `registry/lifecycle.json` are the current lifecycle identity authorities. The current Official Stable release is **GLAZE UI V1.5 / `1.5.1`**.

The token directory intentionally preserves source files from earlier Stable and Candidate qualification lines. Historical `.candidate` suffixes and older product/version fields are retained where they are part of immutable source provenance; they do not override current lifecycle authority.

## Current and historical token roles

`tokens/glaze-v1.json` is the retained V1.2-era Stable token manifest used for historical verification and provenance. It must not be interpreted as the current repository lifecycle version merely because it remains present.

Existing token families continue to provide value authority for color, typography, spacing, geometry, shape, material, depth, motion, iconography, interaction states, layout, and form-factor semantics inherited by later Glaze releases.

## Experience Language Development ownership map

`tokens/glaze-experience-language.dev.json` is a **Development, reference-only, non-consumer-eligible ownership map** for the broader Glaze UI Visual, Spatial, and Interaction Language. It defines the required token categories:

- color
- typography
- spacing
- radius
- border
- shadow
- elevation
- opacity
- blur
- motion
- size
- icon
- breakpoint

The map points each semantic category to existing repository token sources instead of copying raw values or manufacturing a competing authority. It also identifies composition sources for interaction states, spatial behavior, materials, icons, and motion.

This Development map does not modify Stable token values, `VERSION`, lifecycle state, release evidence, or downstream consumer acceptance. Future promotion requires the applicable governed release and exact-revision qualification process.

Token presence, alias resolution, or Development source validation alone never establishes downstream conformance, target-runtime acceptance, deployment, or production eligibility.
