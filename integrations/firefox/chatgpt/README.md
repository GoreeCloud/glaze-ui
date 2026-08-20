# GoreeCloud Glaze UI for ChatGPT

This directory contains the Firefox WebExtension that applies a local GoreeCloud Glaze UI 1.3 presentation layer to ChatGPT.

It is a **presentation-only browser customization**. It does not turn ChatGPT into a GoreeCloud application, does not rebrand OpenAI or ChatGPT, and does not replace the GoreeCloud Browser project.

## Role and purpose

The extension gives standard Firefox users a GoreeCloud-consistent ChatGPT interface while preserving Firefox's normal update path and ChatGPT's native functionality.

The first release focuses on:

- Glaze UI Canvas/Solid/Raised/Functional Glass/Overlay presentation semantics;
- rounded and expressive control geometry;
- light/dark system appearance compatibility;
- comfortable and compact density modes;
- selective functional glass for navigation and composer chrome;
- visible keyboard focus;
- reduced-motion, increased-contrast, forced-colors, and no-backdrop-filter fallbacks;
- local-only extension preferences;
- a Firefox toolbar popup for fast enable/disable, density, Functional Glass, and expressive-motion controls;
- simple rollback through an extension enable/disable preference or normal Firefox extension removal.

## Privacy and security boundary

The extension requests only:

- `storage` — stores its own non-sensitive appearance preferences locally in Firefox;
- host access to `https://chatgpt.com/*` and the legacy `https://chat.openai.com/*` address so its content stylesheet and small preference bootstrap can run there.

The extension does **not** request browsing-history, cookies, downloads, tabs, clipboard, webRequest, proxy, native-messaging, or broad all-sites permissions.

It does not intentionally read, store, transmit, export, index, or analyze ChatGPT conversation content. It does not intercept authentication material or session tokens. It contains no analytics, advertising, telemetry, remote fonts, remote icons, or other remote presentation dependencies.

## Repository structure

```text
integrations/firefox/chatgpt/
├── ACCEPTANCE.md
├── build_extension.py
├── collect_acceptance.py
├── manifest.json
├── README.md
├── icons/
│   └── glaze-chatgpt.svg
└── src/
    ├── content/
    │   ├── chatgpt-glaze.css
    │   └── chatgpt-glaze.js
    ├── options/
    │   ├── options.css
    │   ├── options.html
    │   └── options.js
    └── popup/
        ├── popup.css
        ├── popup.html
        └── popup.js
```

## Temporary installation for development

1. Open Firefox.
2. Visit `about:debugging#/runtime/this-firefox`.
3. Select **Load Temporary Add-on…**.
4. Select `integrations/firefox/chatgpt/manifest.json` from a checked-out copy of this repository.
5. Open or reload ChatGPT.
6. Use the extension toolbar button for fast appearance controls, or open the full Preferences/Options page for the same local settings.

A temporary add-on is removed when Firefox restarts. Signed/persistent release packaging is a separate acceptance gate.

## Deterministic local-test package

Run:

```bash
python3 integrations/firefox/chatgpt/build_extension.py
```

The builder creates a deterministic unsigned local-test XPI at `integrations/firefox/chatgpt/dist/goreecloud-glaze-ui-chatgpt.xpi` plus a matching `.sha256` record. Rebuilding identical reviewed source must produce identical package bytes. The package is for development and runtime acceptance; it is not a claim of Mozilla signing or distribution approval.

The permanent ChatGPT extension validator builds the package twice in isolated temporary directories and fails CI if the bytes or SHA-256 evidence differ.

## Privacy-preserving acceptance evidence

After building the exact XPI that will be tested, generate an acceptance record with `collect_acceptance.py`:

```bash
python3 integrations/firefox/chatgpt/collect_acceptance.py \
  --xpi integrations/firefox/chatgpt/dist/goreecloud-glaze-ui-chatgpt.xpi \
  --revision <exact-git-sha> \
  --firefox-version <version> \
  --firefox-channel release \
  --desktop <desktop-environment> \
  --output acceptance/firefox-chatgpt.md
```

The collector records package identity, Firefox/environment metadata, Glaze preference states, and the required manual checklist. It intentionally does not read or record conversation text, prompts, responses, account identifiers, authentication material, cookies, session tokens, uploaded-file contents, URLs, browsing history, bookmarks, or Firefox profile databases. The generated checklist still requires a human runtime decision; the tool does not claim that scenarios passed merely because it created an evidence file.

## Compatibility model

ChatGPT is an externally controlled web application whose DOM may change without notice. This integration therefore prefers semantic HTML and ARIA selectors over generated CSS class names and avoids replacing application behavior.

When OpenAI changes markup, presentation may partially regress without breaking ChatGPT itself. Such regressions should be corrected by updating selectors after source/visual review rather than expanding permissions or injecting invasive application logic.

## Acceptance gates

`ACCEPTANCE.md` is the authoritative runtime acceptance record for this extension. Before a Stable extension release:

- validate the manifest and all local file references;
- confirm requested permissions remain minimal and documented;
- produce and record the deterministic local-test package SHA-256;
- generate the privacy-preserving acceptance template with `collect_acceptance.py`;
- load the extension in current Firefox;
- validate current `chatgpt.com` conversation, new-chat, sidebar, composer, dialogs, menus, code blocks, and settings surfaces;
- validate toolbar-popup state persistence and synchronization with the full settings page;
- test light and dark appearance;
- test keyboard-only navigation, 200 percent zoom/reflow, and visible focus;
- test `prefers-reduced-motion`, increased contrast, forced colors, and translucency-disabled operation;
- verify the extension does not alter ChatGPT authentication, message submission, file upload, tool use, or conversation navigation behavior;
- verify no network requests are introduced by the extension;
- verify disabling/removing the extension restores the original ChatGPT presentation;
- package and sign through the approved Firefox extension release process before persistent normal use.

## Current validation evidence

The toolbar-control implementation at exact head `519c3cf21ba3ea97874a03dac837588020b5c098` passed Glaze UI CI run #48 (`32369865335`). The documentation successor `2434e7a1a1715f4a5c4cf7c2640b25d808b98a45` passed Glaze UI CI run #51 (`32370046772`). Packaging/acceptance head `b43c4a8f3d7f2a3d23bada10ff093dfd1c7a8b0c` passed Glaze UI CI run #55 (`32371082274`), including deterministic XPI packaging.

The current privacy-preserving evidence-collector successor must receive its own exact-head CI result before it is represented as validated. Source/CI and reproducible-package evidence do **not** replace authenticated runtime acceptance of the extension against the live ChatGPT interface in Firefox.

## Maintenance

This integration follows the canonical Glaze UI version in this repository. It should remain a thin consumer layer rather than becoming an independent design system. ChatGPT-specific selectors and compatibility notes belong here; canonical Glaze UI tokens and component semantics remain owned by the repository's shared Glaze UI sources.