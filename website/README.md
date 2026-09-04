# GLAZE UI V1.1 Design Center

This directory contains the source for the GoreeCloud Design Center public surface and presents the current Stable Glaze UI product identity: **GLAZE UI V1.1** (`1.1.0`).

## Runtime contract

- The document activates V1.1 with `data-glaze-version="1.1"`.
- The public version marker is `goreecloud-glaze-ui=1.1.0`.
- The official Stable entrypoint is `/assets/glaze-v1.1.0.css` and remains same-origin in the built artifact.
- Appearance uses the V1.1 `data-glz-appearance` contract for Light, Dark, and Deep Dark; System removes the explicit appearance attribute.
- The approved **Facet** identity is copied from `assets/identity/official/facet/glaze-ui-mark.svg` and must remain synchronized with that canonical repository source.
- Public CSP remains `style-src 'self'` and `script-src 'self'`; inline style/script declarations are not valid publication inputs.
- Reduced Motion, Reduced Transparency, Increased Contrast, Forced Colors, safe-area, and responsive behavior remain release gates.

The Design Center documents the design system; it does not establish downstream application conformance or production acceptance. Each consumer must generate exact-revision application-specific evidence for its own adoption.