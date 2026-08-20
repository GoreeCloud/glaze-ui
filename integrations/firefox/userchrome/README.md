# Firefox `userChrome.css` Installation

This directory contains the optional deeper Glaze UI styling layer for upstream Mozilla Firefox. It is cosmetic only and does not turn Firefox into GoreeCloud Browser.

## Install

1. Open `about:config` in Firefox.
2. Set `toolkit.legacyUserProfileCustomizations.stylesheets` to `true`.
3. Open `about:support` and use **Profile Directory → Open Directory**.
4. Create a `chrome` directory inside the active Firefox profile if it does not already exist.
5. Copy `userChrome.css` into that `chrome` directory.
6. Restart Firefox completely.

The resulting profile path is normally equivalent to:

```text
<firefox-profile>/chrome/userChrome.css
```

## Remove / Roll Back

Delete or rename `chrome/userChrome.css`, then restart Firefox. No browsing data, bookmarks, credentials, GoreeCloud services, or GoreeCloud Browser data depend on this file.

## Compatibility

Firefox browser-chrome selectors are not a stable public API. Validate this file after Firefox upgrades. If an override becomes incompatible, remove or repair the affected rule rather than weakening Firefox security or accumulating unsafe compatibility workarounds.

The supported Firefox theme in `../theme/` should remain the preferred appearance layer. Use `userChrome.css` only for browser surfaces that cannot be represented adequately through Firefox's supported theme API.
