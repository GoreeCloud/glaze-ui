# Firefox Glaze UI Integration

## Purpose

This integration defines how upstream Mozilla Firefox may use the GoreeCloud Glaze UI design language as a secondary-browser customization without becoming or being represented as GoreeCloud Browser.

GoreeCloud Browser remains the first-class GoreeCloud browser product. It integrates Glaze UI at the Firefox/Gecko source level and has its own product identity, release engineering, security validation, and GoreeCloud-specific browser capabilities.

Standard Firefox remains upstream Firefox and retains its normal Firefox identity, browser engine, update path, security model, and functionality.

## Approved Scope

The Firefox integration is intentionally limited to two customization layers.

### 1. Firefox Theme Layer

The supported Firefox theme package may apply Glaze UI-compatible presentation where Firefox's theme APIs permit it, including:

- Toolbar and browser-chrome colors.
- Active and inactive tab treatment.
- URL-bar and toolbar surface colors.
- Light and dark appearance variants.
- Supported hover, accent, separator, and popup colors.
- Other theme properties supported by the target Firefox release.

This layer should remain the preferred customization method because it uses Firefox-supported theming mechanisms.

### 2. `userChrome.css` Layer

An optional `userChrome.css` layer may provide deeper browser-chrome adaptation where the normal theme API is insufficient, including:

- Tab shape, spacing, and visual hierarchy.
- URL and search field presentation.
- Toolbar spacing and organization.
- Bookmarks bar presentation.
- Sidebar surfaces.
- Menus and popovers.
- Context menus where safely styleable.
- Hover and keyboard-focus states.
- Compact and fullscreen behavior.
- Other Firefox chrome surfaces when maintainable.

The `userChrome.css` layer is optional because Firefox chrome selectors and internal structure may change between releases. Compatibility and maintainability take precedence over cosmetic fidelity.

## Product Boundary

This integration must not rebrand standard Firefox as GoreeCloud Browser.

Standard Firefox:

- Remains Mozilla Firefox.
- Uses Mozilla's upstream browser engine and update mechanisms.
- May receive Glaze UI-compatible styling through supported theming and optional local chrome CSS.
- Serves as the secondary browser once GoreeCloud Browser is stable enough for primary use.

GoreeCloud Browser:

- Is a separate GoreeCloud-maintained Firefox/Gecko distribution.
- Uses its own approved product identity and artwork.
- Integrates Glaze UI directly into GoreeCloud-controlled browser surfaces.
- May provide deeper GoreeCloud service, privacy, security, and workflow integration.

The two products may share Glaze UI design decisions, but they do not share product identity.

## Repository Structure

The intended integration structure is:

```text
integrations/firefox/
├── README.md
├── theme/
│   └── supported Firefox theme package and assets
└── userchrome/
    └── optional userChrome.css customization and supporting files
```

Implementation files should be added only when they are validated against the target Firefox release.

## Design Requirements

Firefox customization must derive from the canonical Glaze UI design system rather than creating a separate Firefox-specific visual language.

The integration should preserve:

- Glaze UI semantic color and surface relationships.
- Layered and softened surface treatment where technically appropriate.
- Consistent spacing and control hierarchy.
- Light and dark appearance support.
- Accessible contrast.
- Visible keyboard focus states.
- Clear active, inactive, hover, disabled, and selected states.
- Predictable fallbacks when Firefox does not permit an intended visual treatment.

The objective is visual compatibility with GoreeCloud, not forced pixel-level sameness with GoreeCloud Browser.

## Safety and Compatibility Requirements

Cosmetic customization must never take precedence over:

1. Firefox security behavior.
2. Browser update reliability.
3. Accessibility.
4. Web compatibility.
5. Keyboard navigation.
6. Native platform behavior where overriding it would reduce usability.
7. Firefox release-to-release maintainability.

The integration must not disable or weaken browser security mechanisms merely to preserve an appearance.

## Independence and Rollback

The Firefox theme and `userChrome.css` customization must remain independently removable.

Removing either layer should return Firefox toward its normal upstream appearance without affecting:

- Firefox profile data.
- Bookmarks or browsing data.
- Stored credentials.
- GoreeCloud service data.
- GoreeCloud Browser source or profile data.
- Any authoritative GoreeCloud backend.

No GoreeCloud service may depend on these cosmetic customizations for availability, authentication, data ownership, backup, or recovery.

## Maintenance Model

For each supported Firefox release or release family:

- Validate the normal theme package first.
- Validate `userChrome.css` separately.
- Prefer supported theme APIs over internal CSS selectors whenever both can provide the required result.
- Record selectors or behaviors that are version-sensitive.
- Remove obsolete overrides instead of accumulating compatibility hacks indefinitely.
- Preserve an easy rollback path to unmodified Firefox chrome.

## Current Status

Status: **Documented / implementation pending**.

This document establishes the approved architecture and product boundary. Theme files and `userChrome.css` implementation should be developed and validated in follow-up work.