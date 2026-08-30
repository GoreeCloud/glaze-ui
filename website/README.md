# Glaze UI Public Design Site

This directory contains the source for the public Glaze UI design-system website at `https://design.goreecloud.com`.

## Current production design boundary

The Design Center consumes **Glaze UI 2.0.0 Stable** through the `glaze-2.0.0.css` Stable entrypoint. Public production pages must not link the historical Candidate implementation directly. The promoted immutable implementation may remain behind the Stable wrapper for provenance, while **Glaze UI 2.1 remains Candidate** and is not a Stable production-conformance target.

## Cloudflare Pages contract

- Repository: `GoreeCloud/goreecloud-glaze-ui`
- Production branch: `main`
- Root directory: repository root
- Build command: `python3 website/build.py`
- Build output directory: `website/dist`
- Custom domain: `design.goreecloud.com`

The build copies the Stable Glaze UI entrypoint, its pinned promoted implementation dependency, and the approved Facet identity source into the isolated public artifact. The website therefore presents repository-controlled Glaze UI primitives and the exact canonical identity rather than detached copies.

## Canonical identity

Facet is the sole approved Glaze UI logo/icon/artwork. The public site receives `/assets/glaze-ui-mark.svg` byte-for-byte from `assets/identity/official/facet/glaze-ui-mark.svg`.

## Validation

Run:

```bash
python3 website/validate.py
```

This builds the isolated artifact and fails closed when required content, Stable dependency wiring, canonical Facet bytes, local appearance behavior, accessibility fallbacks, or security headers are missing.

## Publication and acceptance boundary

The `website/dist` directory is generated and must be treated as the only Cloudflare Pages publication output. Repository governance documents, source-only scripts, tokens, and unrelated files are not part of the public deployment artifact.

A successful build or source validator does not by itself establish an accepted Design Center release. The exact candidate revision must pass the applicable branch-preview/deployment verification before merge, and the resulting `main` revision must be verified on `design.goreecloud.com` after deployment. Source, generated artifact, and deployed bytes must agree before the website change is recorded as production-accepted.
