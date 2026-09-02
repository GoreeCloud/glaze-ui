# Glaze UI Public Design Site

This directory contains the source for the public Glaze UI design-system website at `https://design.goreecloud.com`.

## Cloudflare Pages contract

- Repository: `GoreeCloud/goreecloud-glaze-ui`
- Production branch: `main`
- Root directory: repository root
- Build command: `python3 website/build.py`
- Build output directory: `website/dist`
- Custom domain: `design.goreecloud.com`

The build copies the canonical Glaze UI CSS implementation and the approved Facet identity source into the isolated public artifact. It also renders the Consumer Governance inspection surface directly from `consumers/registry.json`. The website therefore presents repository-controlled Glaze UI primitives, the exact canonical identity, and machine-authoritative consumer adoption state rather than detached copies or manually maintained status claims.

## Consumer Governance boundary

The source page contains a single `GLAZE_CONSUMER_GOVERNANCE` build token. `website/build.py` replaces that token in the publication artifact with the current canonical registry state, including Stable target, audit date, consumer repository, consumer status, production eligibility, exact evidence revision, source-evidence contract where registered, pending acceptance requirements, and registry notes.

The public surface is descriptive, not promotive. `adoption-candidate` is explicitly distinct from `aligned-current-stable`, and no application becomes production eligible because the Design Center renders its state. Product-specific rendered/native, accessibility, supported-platform, and representative-device acceptance remain required by the canonical consumer contract.

The generated governance surface provides keyboard-native search and status filtering for inspection. These controls are visibility-only: they search the rendered consumer name/repository and hide or reveal cards without rewriting status, evidence, production eligibility, or any registry value. The unfiltered summary remains the canonical registry-wide snapshot even while the card view is narrowed.

Each consumer card also exposes the registry's `visualAcceptance` and `notes` fields through a native `details`/`summary` disclosure. The disclosure is informational and fail-closed: the build requires both fields, the validator compares their rendered text to the canonical registry, and opening or reading the disclosure does not satisfy, waive, or replace any pending application-specific acceptance requirement.

`python3 scripts/validate_design_center_consumer_governance.py` rebuilds the site and fails closed if rendered consumer state, repository/evidence fields, acceptance requirements, registry notes, summary counts, visibility-only filtering semantics, 48px interactive targets, responsive governance composition, or forced-colors fallback drift from the canonical registry and Design Center interaction contract.

## Canonical identity

Facet is the sole approved Glaze UI logo/icon/artwork. The public site receives `/assets/glaze-ui-mark.svg` byte-for-byte from `assets/identity/official/facet/glaze-ui-mark.svg`.

## Validation

Run:

```bash
python3 website/validate.py
python3 scripts/validate_design_center_consumer_governance.py
```

The first command validates the isolated Glaze UI publication artifact, canonical CSS/Facet identity, local appearance behavior, security headers, and current/historical release boundaries. The second validates the registry-backed Consumer Governance surface against the exact machine-readable consumer authority and syntax-checks the Design Center interaction script before comparing the generated artifact.

## Publication boundary

The `website/dist` directory is generated and must be treated as the only Cloudflare Pages publication output. Repository governance documents, source-only scripts, tokens, and unrelated files are not part of the public deployment artifact. The Consumer Governance HTML is generated into `website/dist/index.html`; the source registry itself is not copied into the public artifact.
