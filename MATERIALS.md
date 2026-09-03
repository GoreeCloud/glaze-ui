# GLAZE UI V1.0 — Material and Depth Contract

**Status:** Official V1 baseline; acceptance revalidation required.

The canonical V1 material hierarchy is **Canvas → Surface → Soft Glaze → Glaze → Deep Glaze → Live Glaze**. Material communicates hierarchy and interaction; it is never a substitute for information architecture or truth.

**Core presentation rule:** Solid where users read or make explicit critical decisions. Glazed where users interact with transient navigation, command, search, control, or feedback chrome.

Glaze regions must be bounded, locally sampled, readable over worst-permitted backdrops, and removable without loss of semantics. Reduced Transparency, Forced Colors, Increased Contrast, performance constraints, and unsupported backdrop effects must fall back toward solid/opaque surfaces. Nested backdrop blur is not permitted by default. V1 budgets allow one dominant Glaze panel and up to three small floating Glaze controls unless an explicit governed exception exists.
