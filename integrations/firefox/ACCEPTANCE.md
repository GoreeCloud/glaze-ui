# Firefox Glaze UI Runtime Acceptance

## Status

Source validation is automated. Runtime acceptance remains **pending** until results are recorded for representative supported Firefox desktop lines.

## Target Matrix

| Track | Target | Status | Notes |
| --- | --- | --- | --- |
| Firefox Release | Firefox 153 or newer current Release | Pending | Validate the currently deployed supported desktop release. |
| Firefox ESR | Firefox ESR 140 current security-supported point release | Pending | Validate long-lived ESR behavior separately from rapid Release. |

The matrix must be updated when Mozilla changes supported release lines. A version appearing here is a validation target, not a claim that GoreeCloud controls Mozilla's support lifecycle.

## Required Scenarios

For each target track, record pass/fail evidence for light and dark appearance; tab strip and active/inactive tabs; URL/search focus, typing, selection, suggestions, and identity/security indicators; navigation and toolbar actions; bookmarks toolbar; application menu and transient panels; sidebar; downloads; private browsing; certificate, permission, download, update, and warning indicators; keyboard-only navigation and visible focus; increased contrast or forced-colors where the platform exposes it; reduced motion; 200% zoom/reflow where applicable; and rollback by removing the theme and optional `userChrome.css` without profile-data loss.

## Runtime Tooling

Build the deterministic local-test theme package first:

```text
python3 integrations/firefox/build_theme.py
```

The optional deeper chrome layer can be installed only into an explicitly supplied Firefox profile:

```text
python3 integrations/firefox/install_userchrome.py --profile /exact/firefox/profile --install
python3 integrations/firefox/install_userchrome.py --profile /exact/firefox/profile --verify
python3 integrations/firefox/install_userchrome.py --profile /exact/firefox/profile --remove
```

The installer never guesses a Firefox profile, never edits `prefs.js` or `user.js`, and retains a timestamped backup before replacing or removing an existing `userChrome.css`. Firefox preference `toolkit.legacyUserProfileCustomizations.stylesheets` must be enabled separately by the tester when the optional layer is used.

Create a privacy-preserving evidence record before manual scenario testing:

```text
python3 integrations/firefox/collect_acceptance.py \
  --track release \
  --theme-package integrations/firefox/dist/glaze-ui-firefox-0.2.0.xpi \
  --userchrome enabled \
  --desktop "KDE Plasma" \
  --output firefox-release-acceptance.md
```

Run the same process separately for ESR with `--track esr`. The evidence helper records environment and package metadata plus an unchecked scenario checklist; it does not read Firefox history, bookmarks, cookies, credentials, URLs, tabs, or profile contents.

## Acceptance Rules

A Firefox runtime is accepted only when all required scenarios pass or a documented material exception is approved. Cosmetic consistency must never override Firefox security, identity, permission, update, private-browsing, or warning behavior. `userChrome.css` failures are allowed to fall back to the supported theme layer rather than forcing unsafe browser-chrome overrides.

The supported Firefox theme and optional `userChrome.css` layer must be evaluated independently enough that a `userChrome.css` selector regression can be disabled without invalidating an otherwise safe supported-theme experience.

## Evidence Record

Record the exact Firefox version, operating system and desktop environment, Glaze UI repository commit, theme package SHA-256, whether `userChrome.css` was enabled, canonical `userChrome.css` SHA-256 when enabled, tested appearance/accessibility modes, failures and corrections, rollback result, and final acceptance decision.
