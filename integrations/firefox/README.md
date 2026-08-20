# Firefox Glaze UI Integration

## Status

Implementation candidate for **Glaze UI 1.3.0**. Runtime visual and accessibility acceptance against the target Firefox desktop release remains required before this integration is considered stable.

## Purpose

This integration defines how upstream Mozilla Firefox may use Glaze UI as a secondary-browser customization without becoming or being represented as GoreeCloud Browser.

GoreeCloud Browser remains the first-class GoreeCloud browser product. Standard Firefox remains upstream Mozilla Firefox and retains Mozilla identity, Gecko, its normal update path, security model, profile format, and functionality.

## Glaze UI 1.3 Mapping

Firefox browser chrome is treated as an appropriate **Functional Glass** consumer because navigation, controls, toolbars, tabs, menus, and transient browser chrome are exactly the interface categories Glaze UI 1.3 reserves for that material role.

The mapping is deliberately restrained:

- Browser canvas and inactive chrome use Canvas semantics.
- Active tabs, URL/search fields, and durable readable surfaces use Solid or Raised semantics.
- Navigation and toolbar chrome may use Functional Glass semantics where Firefox permits it.
- Menus, URL suggestions, and transient panels use Overlay-style separation.
- Clear Glass is not used because this integration does not place controls over photos, video, artwork, maps, or other rich media.
- Compact/Standard/Pressed shape semantics are used for repetitive browser controls; Expressive geometry is reserved for high-value surfaces such as the focused URL bar or prominent transient panels.
- Effects motion is limited to state feedback. Spatial motion is not injected into Firefox chrome unless a future supported and accessibility-safe mechanism exists.

## Supported Layers

### Firefox Theme

`theme/manifest.json` uses Firefox's supported static-theme surface. It is the preferred layer and includes explicit light and dark variants.

### Optional `userChrome.css`

`userchrome/userChrome.css` provides deeper local browser-chrome adaptation where Firefox's supported theme API is insufficient. This layer is optional and version-sensitive because browser-chrome selectors are not a stable public extension API.

## Safety and Product Boundary

This integration must never:

- Rebrand Mozilla Firefox as GoreeCloud Browser.
- Hide or weaken Firefox security, identity, permission, update, private-browsing, certificate, download, or warning indicators.
- Disable browser security mechanisms for cosmetic compatibility.
- Require remote fonts, icons, scripts, analytics, trackers, or third-party UI dependencies.
- Make GoreeCloud services depend on cosmetic Firefox customization.
- Share Firefox profile data with GoreeCloud Browser merely to achieve visual consistency.

## Accessibility and Resilience

The integration preserves the Glaze UI 1.3 accessibility contract through visible keyboard focus, practical control sizing where Firefox permits it, reduced-motion behavior, increased-contrast and forced-colors fallbacks, readable solid fallbacks when translucency is unavailable, and system/light/dark appearance support.

Firefox-native behavior takes precedence when a cosmetic override would reduce accessibility, security, web compatibility, or release-to-release maintainability.

## Structure

```text
integrations/firefox/
├── README.md
├── validate.py
├── theme/
│   ├── README.md
│   └── manifest.json
└── userchrome/
    ├── README.md
    └── userChrome.css
```

## Acceptance Boundary

Source presence and validation do not constitute Firefox runtime acceptance. Before stable promotion, validate the intended Firefox release on a representative GoreeCloud Linux workstation across light and dark appearance, keyboard-only navigation, focused URL/search fields, menus and panels, bookmarks toolbar, sidebars, private browsing, browser warnings and identity indicators, reduced motion, increased contrast/forced colors where supported, and 200% zoom/reflow where applicable.

Rollback is always removal of the theme and/or `userChrome.css`; profile data must remain intact.
