# Glaze UI Tokens

`glaze.tokens.json` is the platform-neutral semantic token source for **Glaze UI 1.4.0 Stable**.

Numeric spacing, radius, target, blur, focus, layout, and breakpoint values use CSS pixel-equivalent units in the web reference. Native clients map them to normal density-aware platform units while preserving semantic relationships, practical targets, safe areas, and accessibility.

## Typography source policy

The canonical `typography.family` stack is system/platform-native first. Glaze UI does not require a GoreeCloud-specific typeface and must not depend on Google Fonts or another third-party runtime font-delivery service.

A product may intentionally substitute a locally bundled open-source font when that choice materially improves its Role and Purpose, language coverage, accessibility, visual quality, or cross-platform consistency. That substitution is product-specific: it must preserve Glaze semantic typography roles and must be shipped from local or GoreeCloud-controlled assets under a compatible license.

## Glaze UI 1.4 form-factor semantics

`formFactor` defines Mobile, Tablet, Desktop, and TV as interaction environments rather than breakpoint aliases. Each role records viewing distance, primary input, navigation model, density, composition, and an anti-pattern. Compact/Medium/Expanded/Wide remain window-sizing signals.

TV adds larger targets/icons/type, directional-focus scale/lift and timing, overscan-safe references, focus elevation, and sparse row spacing. TV is not selected from width alone.

Applications consume semantic roles rather than literal values. Platform-native implementations may map the same semantics to native focus, density, safe-area, typography, and control systems.
