# Glaze UI Wearable Component Mapping Record

## Current 2.0 mapping

**Glaze UI 2.0.0 is the current Stable contract.** Wearable component behavior derives from `GLAZE_UI_2_STABLE.md`, the promoted 2.0 semantics in `tokens/glaze.tokens.json`, and the exact promotion-source implementation retained in `css/glaze-2.emerging.candidate.css` / `js/glaze-2.emerging.candidate.js`.

The design-system reference proves a compact rotational-navigation pattern and its interaction/accessibility floor. It does not establish a complete native smartwatch component library or physical-device certification.

### Actions and targets

- The general Glaze UI wearable reference floor is 48px.
- Perspective, scaling or presentation effects must never reduce the **rendered interactive region below that floor**.
- Wearable actions expose concise labels or accessible names and remain usable without decorative motion/transparency.
- Destructive meaning does not depend on color alone.

### Lists and rotational navigation

- Vertically ordered lists are the default compact wearable flow.
- **Exactly one rotational-navigation item should be current/focusable at a time** when roving focus is used.
- Rotary/crown-style input is an enhancement; preserve an equivalent task path through touch or another native input when the platform permits it.
- Focus/selection remains visible for non-touch input.

### Status, progress, selection and glance surfaces

- Keep one dominant value/task at a time.
- Use native progress, switch, picker, radio, checkbox, complication, tile, widget and always-on semantics where the target platform supplies them.
- Host-managed glance surfaces are constrained presentations, not miniature full applications.
- Stale/delayed data must not be presented as current.
- Sensitive state respects platform privacy/redaction behavior.

### Materials and motion

Current material terminology is **Canvas / Surface / Soft Glaze / Glaze / Deep Glaze / Live Glaze**. Readability overrides translucency. Reduced motion removes nonessential transformation while preserving selection/focus/task completion. Reduced transparency or unsupported effects resolve to readable bounded surfaces.

### Native product acceptance

A product shipping on a smartwatch/wearable must map these semantics to its actual platform and validate safe areas, text scaling, spoken semantics, native back/dismiss, touch/native-equivalent completion, optional crown/rotary behavior, interruption/restoration, host-managed surfaces, performance and **representative real-device operation**.

## Historical precursor mapping

Older 1.x Wearable Development Candidate component/native artifacts are retained for audit and migration research. They are **historical evidence only** and cannot satisfy a Glaze UI 2.0 native or production claim without explicit 2.0 migration and revalidation.
