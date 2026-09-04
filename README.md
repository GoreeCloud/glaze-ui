# GLAZE UI V1.1

GLAZE UI V1.1 is GoreeCloud's current Stable shared visual and interaction design system. **Beauty is a requirement, not a regression risk.** Machine version: **1.1.0**.

## Core rule

**Solid where users read or make explicit critical decisions. Glazed where users interact with transient navigation, command, search, control, or feedback chrome.**

V1.1 preserves the V1 System Shell, 32-component catalog, semantic color, accessibility, material, performance, and native-mapping contracts while adding the approved Optical Refinement and **Deep Teal + Soft Amber** atmospheric system.

The atmosphere is intentionally subordinate: neutral structure remains dominant; protected semantic meaning, focus, accessibility, and required boundaries always resolve first. Environmental Color Memory remains optional and is not required by the first Stable implementation.

## Next upgrade track — V1.2 Frosted Neutral

The next Glaze UI upgrade is being developed around a new governing optical rule: **Neutral glass is the material. Color is an accent.**

The V1.2 Candidate shifts default glazed surfaces toward frosty white, pearl, clear-neutral, soft gray, and neutral graphite glass with stronger blur, translucency, specular edge light, and depth. Teal, green, aqua, amber, and other chromatic colors are removed from the default material substrate and remain available for intentional active, focus, selection, progress, semantic, icon, and branding treatments.

Candidate source:
- `GLAZE_UI_V1_2_CANDIDATE.md` — next-upgrade contract
- `tokens/glaze-v1.2-frosted-neutral.candidate.json` — machine-readable material tokens
- `css/glaze-v1.2.0-candidate.css` — preview entrypoint layered over V1.1 Stable
- `reference/v1.2/frosted-neutral.html` — frosted-neutral visual reference
- `scripts/validate_glaze_v1_2_candidate.py` — fail-closed Candidate validator

V1.1 remains the current Stable and mandatory source authority until the V1.2 candidate passes its governed visual, accessibility, performance, regression, and promotion gates. The Candidate does not automatically migrate downstream GoreeCloud applications.

## Stable evidence

Project-owner optical approval was recorded on 2026-09-03. Exact release-candidate revision `b37538f6748d95680ca5f6fe4a5e412a38ef87a7` reproduced the five approved web reference PNG hashes and passed fresh Android handheld emulator acceptance for Light/48dp, Dark + Reduced Transparency/48dp, and Deep Dark + 200% text + Touch Assistance/56dp in release-evidence workflow `33750604928`.

Current source authority:
- `VERSION` — `1.1.0`
- `GLAZE_UI_V1_1.md` — official Stable contract
- `registry/lifecycle.json` — lifecycle authority
- `css/glaze-v1.1.0.css` — Stable web entrypoint
- `js/glaze-v1.1.0.mjs` — Stable runtime entrypoint
- `contracts/v1.1/optical-refinement.json` — Stable optical contract
- `tokens/glaze-v1.1-atmosphere.json` — Stable atmosphere tokens
- `contracts/regression/visual-baselines-v1.json` — approved visual baseline authority
- `acceptance/v1.1-stable.md` — Stable acceptance boundary

The V1.0 contract and candidate/RC records remain historical audit evidence, not current consumer targets. No downstream GoreeCloud application auto-upgrades or gains production eligibility by declaration.

Glaze Motion remains separately Experimental.

## License

MIT. GoreeCloud branding and product identity remain subject to applicable project policies.
