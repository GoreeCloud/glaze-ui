# Glaze UI Tokens

`glaze.tokens.json` is the platform-neutral semantic token source for Glaze UI 1.0.

Numeric spacing, radius, target, blur, focus, layout, and breakpoint values are expressed in CSS pixel-equivalent units for the web reference implementation. Native clients should map these values into the platform's normal density-aware units while preserving the semantic relationship and practical target size.

Motion duration values are milliseconds. Opacity values are unitless ratios. Color values are CSS-compatible strings because the web reference is the first canonical implementation; native mappings may translate them into platform-native color representations.

Applications should consume semantic roles rather than copying literal values. If a platform cannot reproduce a token exactly, preserve its purpose and document the mapping.
