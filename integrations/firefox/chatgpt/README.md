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
├── manifest.json
├── README.md
├── icons/
│   └── glaze-chatgpt.svg
└── src/
    ├── content/
    │   ├── chatgpt-glaze.css
    │   └── chatgpt-glaze.js
    └── options/
        ├── options.css
        ├── options.html
        └── options.js
```

## Temporary installation for development

1. Open Firefox.
2. Visit `about:debugging#/runtime/this-firefox`.
3. Select **Load Temporary Add-on…**.
4. Select `integrations/firefox/chatgpt/manifest.json` from a checked-out copy of this repository.
5. Open or reload ChatGPT.
6. Use the extension's Preferences/Options page to adjust density, functional glass, expressive motion, or disable the presentation layer.

A temporary add-on is removed when Firefox restarts. Signed/persistent release packaging is a separate acceptance gate.

## Compatibility model

ChatGPT is an externally controlled web application whose DOM may change without notice. This integration therefore prefers semantic HTML and ARIA selectors over generated CSS class names and avoids replacing application behavior.

When OpenAI changes markup, presentation may partially regress without breaking ChatGPT itself. Such regressions should be corrected by updating selectors after source/visual review rather than expanding permissions or injecting invasive application logic.

## Acceptance gates

Before a Stable extension release:

- validate the manifest and all local file references;
- confirm requested permissions remain minimal and documented;
- load the extension in current Firefox;
- validate current `chatgpt.com` conversation, new-chat, sidebar, composer, dialogs, menus, code blocks, and settings surfaces;
- test light and dark appearance;
- test keyboard-only navigation and visible focus;
- test `prefers-reduced-motion`, increased contrast, forced colors, and translucency-disabled operation;
- verify the extension does not alter ChatGPT authentication, message submission, file upload, tool use, or conversation navigation behavior;
- verify no network requests are introduced by the extension;
- verify disabling/removing the extension restores the original ChatGPT presentation;
- package and sign through the approved Firefox extension release process before persistent normal use.

## Maintenance

This integration follows the canonical Glaze UI version in this repository. It should remain a thin consumer layer rather than becoming an independent design system. ChatGPT-specific selectors and compatibility notes belong here; canonical Glaze UI tokens and component semantics remain owned by the repository's shared Glaze UI sources.
