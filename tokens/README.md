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


## V1.6 loading and skeleton Development semantic map

`tokens/glaze-v1.6-loading.dev.json` is the first V1.6-specific **Development, non-consumer-eligible semantic map**. It covers skeleton surfaces, geometry, motion modes, loading state, progress, recovery presentation, accessibility fallbacks, performance levels, and motion-fatigue protection.

The map inherits Stable V1.5.1 authorities from `tokens/motion.json`, `tokens/states.json`, `tokens/layout.json`, and `tokens/materials.json` rather than replacing their current Stable values. It adds V1.6 semantic intent for the Development loading/skeleton resolver while preserving these boundaries:

- Reduced Motion maps continuous skeleton motion to `static`.
- Reduced Transparency maps skeleton presentation to solid surfaces.
- Increased Contrast and Forced Colors prohibit opacity-only differentiation.
- Determinate progress requires truthful progress values; fake percentages are forbidden.
- Efficient and Essential performance levels disable continuous skeleton motion.
- Many simultaneous skeletons trigger motion-fatigue protection rather than multiplying shimmer.

This map is Development source only. It does not change `VERSION`, lifecycle state, current Stable token authority, consumer eligibility, downstream conformance, deployment, or production status.
