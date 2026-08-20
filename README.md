# Glaze UI

Glaze UI is GoreeCloud's shared visual and interaction design system.

It preserves the polished, layered, rounded, gradient-rich character already used across GoreeCloud while making the underlying rules reusable, accessible, versioned, and testable.

**Beauty is a requirement, not a regression risk.** Glaze UI standardizes semantics and behavior without flattening individual GoreeCloud applications into identical screens.

## Design lineage

Glaze UI is heavily inspired by a deliberate combination of **Samsung One UI 8.5**, **Apple Liquid Glass**, and **Google Material 3 Expressive**, then reinterpreted through GoreeCloud's own privacy, accessibility, identity, resilience, and cross-platform requirements.

The design formula is:

**One UI 8.5 ergonomics + Liquid Glass hierarchy and fluid material + Material 3 Expressive shape, motion, and adaptive expression + GoreeCloud privacy, identity, accessibility, and simplicity = Glaze UI.**

These systems are references, not templates. A GoreeCloud interface must not look like a Samsung, Apple, or Google skin.

## Glaze UI 1.3

Glaze UI 1.3 is the expressive-hierarchy evolution of the system. It adds stronger personality and modern interaction while preserving the disciplined 1.0–1.2 foundation.

**Release status:** 1.3.0 is an active release candidate in pull request #6. Glaze UI 1.2.0 on `main` remains the Stable baseline until the exact 1.3 candidate passes source CI, Chromium-rendered acceptance, review, and explicit Stable promotion.

New 1.3 capabilities include:

- **functional glass** for navigation, controls, toolbars, and transient chrome, separating interactive glass from ordinary content;
- a more transparent **clear glass** role reserved for controls floating over visually rich media;
- an expressive shape scale for compact, standard, expressive, hero, and pressed states;
- separate **effects motion** and **spatial motion** semantics so color/opacity feedback can remain quick while geometry and hierarchy transitions feel more fluid;
- expressive action and tile primitives with bounded shape morphing and press response;
- adaptive button groups that give important actions more room without changing action order;
- compact-screen **reachability composition** that can place frequent actions in the lower interaction zone while preserving logical and keyboard order;
- stronger hero/supporting typography semantics for intentional dramatic hierarchy;
- explicit reduced-motion, reduced-transparency, forced-colors, and no-backdrop-filter fallbacks for the new expressive layer.

The established architecture remains intact: semantic light/dark tokens; Canvas, Solid, Raised, Glaze, and Overlay surfaces; Compact/Medium/Expanded/Wide layouts; practical targets and focus; accessibility/resilience fallbacks; privacy-conscious local presentation dependencies; form and selection semantics; safe-area handling; and Stable-release visual acceptance.

## Repository layout

- `VERSION` — current Glaze UI version.
- `tokens/glaze.tokens.json` — platform-neutral semantic token source.
- `css/glaze.css` — canonical web variables and core primitives.
- `css/glaze.controls.css` — canonical form, selection, progress, and banner primitives.
- `css/glaze.expressive.css` — Glaze UI 1.3 functional glass, expressive shape/motion, adaptive groups, reachability, and hero-type primitives.
- `css/glaze.accessibility.css` — accessibility and resilience fallbacks.
- `COMPONENTS.md` — component behavior and state contract.
- `CONFORMANCE.md` — Stable-release conformance gates.
- `ADOPTION.md` — integration guidance for GoreeCloud applications.
- `ACCEPTANCE.md` — Stable-release rendered visual/accessibility acceptance protocol.
- `acceptance/` — version-specific Stable promotion evidence.
- `reference/index.html` — dependency-free visual reference.
- `reference/acceptance.html` — browser-render acceptance harness.
- `scripts/validate_glaze_ui.py` — zero-dependency repository validator.
- `scripts/validate_rendered_reference.py` — Chromium-rendered reference acceptance validator.

## Surface and material hierarchy

1. **Canvas** — atmospheric application background; may carry restrained GoreeCloud gradients.
2. **Solid** — high-readability content surface.
3. **Raised** — solid or nearly solid panel with soft elevation.
4. **Glaze / Functional Glass** — selectively translucent functional layer used primarily for controls and navigation.
5. **Overlay** — dialogs, menus, sheets, and other attention-priority surfaces with the strongest separation.

Clear glass is an additional specialized material for controls over photos, video, artwork, maps, or similarly rich backgrounds. It is not a general content-card style.

Glass is never mandatory everywhere. Depth should be visible, not noisy.

## Expression model

Glaze UI uses expression intentionally rather than uniformly. Ordinary utility interactions remain calm and predictable. Prominent actions, hero moments, selected states, product identity, and high-value transitions may use stronger shape, motion, typography, or color expression when it improves comprehension or delight.

## Product personality

Glaze UI creates a family resemblance, not cloned interfaces. Applications may vary composition, artwork, accent emphasis, information density, navigation arrangement, visualization, and specialized components when those choices support the application's Role and Purpose.

## Validation

Repository/source validation:

```bash
python3 scripts/validate_glaze_ui.py
```

Rendered reference acceptance, on systems with a supported Chromium-family browser:

```bash
python3 scripts/validate_rendered_reference.py
```

The source validator uses only the Python standard library. The rendered validator also uses only the Python standard library and an installed Chromium-family browser; it does not add a JavaScript package or remote UI dependency.

## Versioning

Glaze UI follows semantic versioning. Patch releases fix or clarify compatible behavior. Minor releases add compatible tokens, primitives, or components. Major releases may change required semantics. GoreeCloud applications should record the exact Glaze UI version they target.

## License

Glaze UI source and reference implementation are licensed under the MIT License. GoreeCloud branding and product identity remain subject to their applicable project policies.
