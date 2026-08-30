# Glaze UI Public Design Site

This directory contains the source for the public Glaze UI design-system website at `https://design.goreecloud.com`.

## Cloudflare Pages contract

- Repository: `GoreeCloud/goreecloud-glaze-ui`
- Production branch: `main`
- Root directory: repository root
- Build command: `python3 website/build.py`
- Build output directory: `website/dist`
- Custom domain: `design.goreecloud.com`

The build copies the canonical Glaze UI CSS implementation and the approved Facet identity source into the isolated public artifact. The website therefore presents repository-controlled Glaze UI primitives and the exact canonical identity rather than detached copies.

## Canonical identity

Facet is the sole approved Glaze UI logo/icon/artwork. The public site receives `/assets/glaze-ui-mark.svg` byte-for-byte from `assets/identity/official/facet/glaze-ui-mark.svg`.

## Validation

Run:

```bash
python3 website/validate.py
```

This builds the isolated artifact and fails closed when required content, canonical CSS, canonical Facet bytes, local appearance behavior, or security headers are missing.

## Publication boundary

The `website/dist` directory is generated and must be treated as the only Cloudflare Pages publication output. Repository governance documents, source-only scripts, tokens, and unrelated files are not part of the public deployment artifact.