# GLAZE UI V1.0 — Material and Depth Contract

**Status:** Official V1 baseline; acceptance revalidation required.

The canonical V1 material hierarchy is **Canvas → Surface → Soft Glaze → Glaze → Deep Glaze → Live Glaze**. Material communicates hierarchy and interaction; it is never a substitute for information architecture or truth.

**Core presentation rule:** Solid where users read or make explicit critical decisions. Glazed where users interact with transient navigation, command, search, control, or feedback chrome.

Ordinary content defaults to **Solid** or **Raised**. Functional Glass is reserved for bounded navigation, toolbars, compact controls, and transient chrome. Clear Glass is specialized presentation over visually rich media and is not the default content material. Modal Overlay requires explicit semantic separation from the underlying content.

Glaze regions must be bounded, locally sampled, readable over worst-permitted backdrops, and removable without loss of semantics. Reduced Transparency, Forced Colors, Increased Contrast, performance constraints, and unsupported backdrop effects must fall back toward solid/opaque surfaces. Nested backdrop blur is not permitted by default. V1 budgets allow one dominant Glaze panel and up to three small floating Glaze controls unless an explicit governed exception exists.

Reduced transparency is independent from reduced motion. Platforms may expose different native accessibility APIs, but the explicit semantic preference path is the portable contract. Reduced Transparency removes blur and backdrop-dependent presentation while preserving information and hierarchy through opacity, tonal separation, geometry, borders, and contrast.

Performance degradation must fall back toward Solid/Raised semantics before hierarchy or meaning is lost. Unsupported backdrop effects follow the same fail-closed material rule. Decorative refraction and nested backdrop stacks are not required for correct presentation.

Glaze UI owns presentation only. Privacy Shield remains authoritative for privacy state, Wardveil Security remains authoritative for security state, Everkeep remains authoritative for resilience and recovery state, and GoreeCloud Mesh remains authoritative for coordination state. Material styling must not manufacture, strengthen, conceal, or reinterpret those systems' producer-authoritative truth.
