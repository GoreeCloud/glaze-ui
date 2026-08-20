# Firefox Glaze UI Theme

This directory contains the supported-theme portion of the Glaze UI adaptation for upstream Mozilla Firefox.

The theme is intentionally cosmetic. Firefox retains its upstream identity, engine, update path, security model, profile, and normal functionality.

## Development Test

For temporary local testing, load `manifest.json` as a temporary add-on from Firefox's debugging interface. Temporary add-ons are removed when Firefox exits, making this suitable for visual validation without establishing a permanent dependency.

## Validation Checklist

Validate at minimum:

- Active and inactive tabs remain clearly distinguishable.
- URL-bar text, placeholder text, and focus treatment remain readable.
- Toolbar icons retain sufficient contrast.
- Popups and sidebar surfaces remain legible.
- Keyboard focus remains visible.
- Light and dark operating-system appearances remain usable.
- Private browsing and Firefox security indicators remain understandable.
- Firefox updates, permissions, identity indicators, and warnings are not hidden or visually weakened.

## Packaging

Package the contents of this directory only after validation against the intended Firefox release. Do not include `userChrome.css` in the theme package; the deeper CSS layer is intentionally independent and removable.
