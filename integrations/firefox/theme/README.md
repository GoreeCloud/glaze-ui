# Firefox GLAZE UI V1.0 Theme

This directory contains the supported static-theme layer for upstream Mozilla Firefox.

Firefox remains Mozilla Firefox. This package changes browser appearance only and does not alter Gecko, Firefox security behavior, update behavior, profile ownership, or product identity.

## Design Mapping

The theme maps GLAZE UI V1.0 semantics into Firefox-supported theme properties:

- Canvas → frame and new-tab backgrounds.
- Solid/Raised → selected tab, toolbar field, cards, and readable popup surfaces.
- Accent/focus → selected-tab line, loading indicator, attention icons, and focused field borders.
- State layers → hover/pressed toolbar button backgrounds and highlighted popup/sidebar rows.
- Light/dark → separate `theme` and `dark_theme` definitions.
- Text selection → explicit toolbar-field highlight colors.

Static Firefox themes cannot represent every Glaze material behavior. Functional Glass blur, expressive geometry, and deeper chrome layout are therefore handled only by the optional `../userchrome/` layer when safe and maintainable.

## Development Test

For temporary local testing, load `manifest.json` as a temporary add-on from Firefox's debugging interface. Temporary add-ons disappear when Firefox exits, making this suitable for nonpersistent visual review.

Permanent distribution requires normal Mozilla signing requirements for Firefox themes.

## Validation Checklist

Validate at minimum:

- active and inactive tabs remain clearly distinguishable;
- URL/search field text and focus remain readable;
- selected URL text is readable;
- toolbar icons retain sufficient contrast;
- popups, sidebars, bookmarks, and new-tab surfaces remain legible;
- light and dark operating-system appearances select the intended variant;
- keyboard focus remains visible;
- private-browsing, identity, permission, update, warning, download, and certificate indicators remain understandable;
- no remote UI dependency is introduced.

Run the repository-local validator from the repository root:

```bash
python3 integrations/firefox/validate.py
```
