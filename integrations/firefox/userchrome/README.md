# Firefox `userChrome.css` — GLAZE UI V1.0

This directory contains the optional deeper Glaze UI styling layer for upstream Mozilla Firefox. It is cosmetic only and does not turn Firefox into GoreeCloud Browser.

## Install

1. Open `about:config` in Firefox.
2. Set `toolkit.legacyUserProfileCustomizations.stylesheets` to `true`.
3. Open `about:support` and use **Profile Directory → Open Directory**.
4. Create a `chrome` directory inside the active Firefox profile if it does not already exist.
5. Copy `userChrome.css` into that `chrome` directory.
6. Restart Firefox completely.

The resulting path is normally:

```text
<firefox-profile>/chrome/userChrome.css
```

## GLAZE UI V1.0 Role

The stylesheet treats the browser navigation area as Functional Glass, keeps active tabs and fields on readable Raised/Solid surfaces, uses Compact/Standard/Pressed geometry for routine controls, reserves Expressive geometry for the focused URL bar and prominent transient panels, and deliberately does not use Clear Glass.

It includes solid fallbacks when backdrop filtering is unavailable, reduced-motion behavior, increased-contrast handling, and forced-colors fallbacks.

## Remove / Roll Back

Delete or rename `chrome/userChrome.css`, then restart Firefox. No browsing data, bookmarks, credentials, GoreeCloud service data, or GoreeCloud Browser profile data depends on this file.

## Compatibility Boundary

Firefox browser-chrome selectors are not a stable public API. Validate this file after Firefox upgrades. If an override becomes incompatible, remove or repair the affected rule rather than weakening Firefox security, accessibility, or update reliability.

The supported Firefox theme in `../theme/` remains the preferred appearance layer. Use `userChrome.css` only for browser surfaces that cannot be represented adequately through Firefox's supported theme API.
