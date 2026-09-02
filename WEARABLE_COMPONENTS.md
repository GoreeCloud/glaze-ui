# Glaze UI Wearable Component Mapping Record

## Current 2.2 mapping

**Glaze UI 2.2.0 is the current Stable contract.** Wearable component behavior derives from `GLAZE_UI_2_2_STABLE.md`, current 2.2 semantics in `tokens/glaze.tokens.json`, and the retained 2.x platform-neutral implementation in `css/glaze-2.emerging.candidate.css` / `js/glaze-2.emerging.candidate.js`.

The design-system reference proves a compact rotational-navigation pattern and its interaction/accessibility floor. It does not establish a complete native smartwatch component library or physical-device certification. The bounded 2.2 Android handheld reference does not change that wearable boundary.

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

Current material terminology is **Canvas / Surface / Soft Glaze / Glaze / Deep Glaze / Live Glaze**. Readability overrides translucency. Semantic color remains explicit through labels/state treatment and is not color-only. Reduced Motion removes nonessential transformation while preserving selection/focus/task completion. Reduced Transparency or unsupported effects resolve to readable bounded surfaces.

### Native product acceptance

A product shipping on a smartwatch/wearable must map these semantics to its actual platform and validate safe areas, text scaling, spoken semantics, native back/dismiss, touch/native-equivalent completion, optional crown/rotary behavior, interruption/restoration, host-managed surfaces, performance and **representative real-device operation**.

## Historical precursor mapping

Older 1.x Wearable Development Candidate component/native artifacts and the 2.0/2.1 Stable mappings are retained for audit, rollback and migration research. They are **historical evidence only** and cannot satisfy a Glaze UI 2.2 native or production claim without explicit 2.2 migration and revalidation.
