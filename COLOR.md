# GLAZE UI V1.0 — Color Contract

**Status:** Official V1 baseline; acceptance revalidation required.

GLAZE UI V1.0 uses semantic color rather than product-specific hard-coded color meaning. Color must preserve readable contrast, state distinction, platform accessibility preferences, and truth boundaries.

Required semantic families include canvas, surface, text, line, accent, focus, success, warning, critical, and informational roles. No critical state may depend on color alone. Increased Contrast and Forced Colors must remain functional. Wallpaper or backdrop sampling may influence tone but must never override semantic meaning.

Machine-readable color tokens remain under `tokens/semantic-colors.json` and `tokens/adaptive-colors.json`; their V1 acceptance must be revalidated against the reset baseline.
