# GoreeCloud Glaze UI for ChatGPT — Firefox Acceptance

This record defines the runtime acceptance gate for the Firefox WebExtension in this directory. Source validation and deterministic packaging are prerequisites, not substitutes for live acceptance against ChatGPT.

## Release boundary

The extension remains a candidate until every required scenario below is completed on the intended Firefox desktop environment and the tested package SHA-256 is recorded. Mozilla Firefox remains Firefox. ChatGPT remains an OpenAI service. The extension is a removable GoreeCloud presentation layer only.

A temporary or unsigned local-test XPI may be used for acceptance. Persistent distribution requires the approved Mozilla signing/release path and must use the same reviewed source revision.

## Required evidence

Record:

- GoreeCloud/glaze-ui commit SHA;
- pull request or release reference;
- extension version from manifest.json;
- built XPI SHA-256;
- Firefox version and channel;
- operating system and desktop environment;
- test date;
- tester;
- whether the optional Functional Glass and expressive-motion preferences were enabled;
- pass/fail result and notes for each scenario.

Do not record ChatGPT conversation contents, prompts, responses, account identifiers, authentication material, cookies, session tokens, uploaded file contents, or browsing history as acceptance evidence.

## Functional scenarios

1. Extension loads without manifest, CSP, or console errors attributable to the extension.
2. Toolbar popup opens and reflects stored extension state.
3. Enable/disable state applies immediately or after the documented reload boundary and persists locally.
4. Comfortable and compact density settings remain synchronized between popup and full preferences.
5. Functional Glass and expressive-motion settings remain synchronized between popup and full preferences.
6. New-chat creation behaves normally.
7. Existing conversation navigation behaves normally.
8. Message composition, multiline editing, submission, stop-generation, retry/regenerate, and edit workflows remain functional where available.
9. File-upload and attachment controls remain functional where available.
10. Tool/model/project/workspace controls that are available to the test account remain functional.
11. Menus, dialogs, popovers, settings, code blocks, tables, citations, and copy controls remain usable.
12. Disabling or removing the extension restores the original ChatGPT presentation without data loss.

## Visual scenarios

Validate both light and dark appearance where ChatGPT and Firefox expose them.

- Canvas/background hierarchy remains readable and does not obscure native ChatGPT content.
- Sidebar/navigation uses restrained Functional Glass only when enabled.
- Composer remains clearly distinguishable and usable at common window widths.
- Buttons, fields, menus, dialogs, code blocks, and selected/active states remain legible.
- No horizontal overflow is introduced at representative compact and expanded widths.
- Focus outlines are visible and are not clipped.
- Compact density remains usable without creating impractically small controls.
- Expressive motion does not move layout-critical content or interfere with pointer targeting.

## Accessibility and resilience scenarios

- Keyboard-only navigation can reach all normally reachable ChatGPT controls.
- Visible focus remains present on links, buttons, fields, menu items, and dialog controls.
- Browser zoom/reflow remains usable at 200 percent.
- Reduced-motion preference removes extension-authored motion that is not essential.
- Increased-contrast and forced-colors modes remain legible where Firefox/OS support them.
- With Functional Glass disabled, all relevant surfaces remain solid and readable.
- If backdrop-filter support is unavailable, solid fallbacks remain readable.
- Screen-reader semantics and accessible names supplied by ChatGPT are not removed or replaced by the extension.

## Privacy and security verification

- Firefox permissions remain limited to `storage` and ChatGPT-only host access.
- No extension-authored network request is observed during normal operation.
- No conversation text, prompt text, response text, account data, cookies, session data, or authentication material is persisted by the extension.
- No analytics, telemetry, advertising, remote fonts, remote icons, or remote presentation dependency is loaded by the extension.
- The extension does not modify ChatGPT authentication or session handling.

## Compatibility / DOM-drift review

Because ChatGPT markup is externally controlled, acceptance must explicitly inspect the current live interface for selector drift. A partially unstyled surface is a compatibility defect; it is not justification to broaden permissions or inspect conversation content.

Record any affected surface and the smallest semantic or structural selector change needed. Generated or unstable class names should not become the primary compatibility contract unless no safer alternative exists and the exception is documented.

## Stable decision

Stable acceptance requires all required scenarios to pass on the intended Firefox release line. Any failed authentication, message submission, navigation, upload, keyboard, focus, privacy, or rollback scenario is blocking.

Visual differences that do not reduce function, readability, accessibility, privacy, or product identity may be recorded as non-blocking only with explicit review notes.
