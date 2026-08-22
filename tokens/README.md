# Glaze UI Tokens

`glaze.tokens.json` is the platform-neutral semantic token source for **Glaze UI 1.4.0 Stable**.

Numeric spacing, radius, target, blur, focus, layout, and breakpoint values use CSS pixel-equivalent units in the web reference. Native clients map them to normal density-aware platform units while preserving semantic relationships, practical targets, safe areas, and accessibility.

## Glaze UI 1.4 form-factor semantics

`formFactor` defines Mobile, Tablet, Desktop, and TV as interaction environments rather than breakpoint aliases. Each role records viewing distance, primary input, navigation model, density, composition, and an anti-pattern. Compact/Medium/Expanded/Wide remain window-sizing signals.

TV adds larger targets/icons/type, directional-focus scale/lift and timing, overscan-safe references, focus elevation, and sparse row spacing. TV is not selected from width alone.

Applications consume semantic roles rather than literal values. Platform-native implementations may map the same semantics to native focus, density, safe-area, typography, and control systems.
