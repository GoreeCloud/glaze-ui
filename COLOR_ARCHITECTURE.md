# GLAZE UI V1.0 — Color Architecture

GLAZE UI V1.0 separates palette generation from semantic assignment. Consumers bind semantic roles to platform-appropriate values while preserving meaning across Light, Dark, Deep Dark, Increased Contrast, Forced Colors, Reduced Transparency, and contextual appearance modes.

Adaptive color may respond to environment or content only within bounded ranges. Security, privacy, recovery, destructive-action, and system-status colors must remain sourced from their authoritative truth domains and may not be manufactured by Glaze UI presentation.

Current machine-readable sources: `tokens/semantic-colors.json` and `tokens/adaptive-colors.json`.
