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

The source page contains a single `GLAZE_CONSUMER_GOVERNANCE` build token. `website/build.py` replaces that token in the publication artifact with the current canonical registry state, including Stable target, audit date, consumer status, production eligibility, exact evidence revision, and source-evidence contract where registered.

The public surface is descriptive, not promotive. `adoption-candidate` is explicitly distinct from `aligned-current-stable`, and no application becomes production eligible because the Design Center renders its state. Product-specific rendered/native, accessibility, supported-platform, and representative-device acceptance remain required by the canonical consumer contract.

`python3 scripts/validate_design_center_consumer_governance.py` rebuilds the site and fails closed if rendered consumer state, source-evidence fields, summary counts, responsive governance composition, or forced-colors fallback drift from the canonical registry.

## Canonical identity

Facet is the sole approved Glaze UI logo/icon/artwork. The public site receives `/assets/glaze-ui-mark.svg` byte-for-byte from `assets/identity/official/facet/glaze-ui-mark.svg`.

## Validation

Run:

```bash
python3 website/validate.py
python3 scripts/validate_design_center_consumer_governance.py
```

The first command validates the isolated Glaze UI publication artifact, canonical CSS/Facet identity, local appearance behavior, security headers, and current/historical release boundaries. The second validates the registry-backed Consumer Governance surface against the exact machine-readable consumer authority.

## Publication boundary

The `website/dist` directory is generated and must be treated as the only Cloudflare Pages publication output. Repository governance documents, source-only scripts, tokens, and unrelated files are not part of the public deployment artifact. The Consumer Governance HTML is generated into `website/dist/index.html`; the source registry itself is not copied into the public artifact.
