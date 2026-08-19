# Glaze UI

Glaze UI is GoreeCloud's shared visual and interaction design system.

It preserves the polished, layered, rounded, gradient-rich character already used across GoreeCloud while making the underlying rules reusable, accessible, versioned, and testable.

**Beauty is a requirement, not a regression risk.** Glaze UI standardizes semantics and behavior without flattening individual GoreeCloud applications into identical screens.

## Design formula

Material structure + liquid depth and fluidity + One UI ergonomics + GoreeCloud privacy, identity, and simplicity = Glaze UI.

## Glaze UI 1.1

The 1.1 foundation includes everything in 1.0 and expands the reusable contract with:

- semantic `info`, `onAccent`, and modal scrim roles;
- shared hover, pressed, focus, and selected state-layer semantics;
- standard icon sizes and compact/comfortable density guidance;
- adaptive gutters and safe-area helpers for modern mobile/device layouts;
- reusable navigation-item, toolbar, badge, dialog, menu, toast, scrim, and icon primitives;
- broader typography roles and stronger cross-platform semantic mapping;
- exact-version conformance evidence for stable GoreeCloud consumers.

The established 1.0 architecture remains intact: semantic light/dark tokens; Canvas, Solid, Raised, Glaze, and Overlay surfaces; Compact/Medium/Expanded/Wide layouts; restrained motion; practical targets and focus; accessibility/resilience fallbacks; local/privacy-conscious presentation dependencies; and stable-release visual acceptance.

## Repository layout

- `VERSION` — current Glaze UI version.
- `tokens/glaze.tokens.json` — platform-neutral semantic token source.
- `css/glaze.css` — canonical web variables and primitives.
- `css/glaze.accessibility.css` — accessibility and resilience fallbacks.
- `COMPONENTS.md` — component behavior and state contract.
- `CONFORMANCE.md` — stable-release conformance gates.
- `ADOPTION.md` — integration guidance for GoreeCloud applications.
- `reference/index.html` — dependency-free visual reference.
- `scripts/validate_glaze_ui.py` — zero-dependency repository validator.

## Surface hierarchy

1. **Canvas** — atmospheric application background; may carry restrained GoreeCloud gradients.
2. **Solid** — high-readability surface used when translucency would reduce clarity or performance.
3. **Raised** — solid or nearly solid panel with soft elevation.
4. **Glaze** — selectively translucent surface with blur/saturation and a mandatory solid fallback.
5. **Overlay** — dialogs, menus, sheets, and other attention-priority surfaces with the strongest separation.

Glass is never mandatory everywhere. Depth should be visible, not noisy.

## Product personality

Glaze UI creates a family resemblance, not cloned interfaces. Applications may vary composition, artwork, accent emphasis, information density, navigation arrangement, visualization, and specialized components when those choices support the application's Role and Purpose.

## Validation

Run:

```bash
python3 scripts/validate_glaze_ui.py
```

The validator uses only the Python standard library.

## Versioning

Glaze UI follows semantic versioning. Patch releases fix or clarify compatible behavior. Minor releases add compatible tokens, primitives, or components. Major releases may change required semantics. GoreeCloud applications should record the exact Glaze UI version they target.

## License

Glaze UI source and reference implementation are licensed under the MIT License. GoreeCloud branding and product identity remain subject to their applicable project policies.
