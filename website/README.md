# Glaze UI Public Design Site

This directory contains the source for the public Glaze UI design-system website planned for `https://design.goreecloud.com`.

## Cloudflare Pages contract

- Repository: `GoreeCloud/glaze-ui`
- Production branch: `main`
- Root directory: repository root
- Build command: `python3 website/build.py`
- Build output directory: `website/dist`
- Planned custom domain: `design.goreecloud.com`

The build copies the canonical `css/glaze.css` and `css/glaze.accessibility.css` files into the isolated public artifact. The website therefore demonstrates the exact repository design-system implementation rather than maintaining a detached copy of Glaze UI primitives.

## Validation

Run:

```bash
python3 website/validate.py
```

This builds the isolated artifact and fails closed when required content, canonical CSS, local appearance behavior, or security headers are missing.

## Publication boundary

The `website/dist` directory is generated and must be treated as the only Cloudflare Pages publication output. Repository governance documents, source-only scripts, tokens, and unrelated files are not part of the public deployment artifact.

Connecting the Pages project, enabling the custom domain, and making DNS changes are separate production operations and are not performed by repository changes alone.
