# Glaze UI Wearable Component Mapping Record

## Current 2.0 mapping

Glaze UI 2.0.0 Candidate is the enforced active-development contract. Current wearable component behavior derives from `GLAZE_UI_2.md`, `tokens/glaze-2.candidate.json`, and the Candidate implementation in `css/glaze-2.emerging.candidate.css` / `js/glaze-2.emerging.candidate.js`.

The design-system reference currently proves one compact rotational-navigation pattern and its interaction/accessibility floor. It does not establish a complete native smartwatch component library or physical-device certification.

### Actions and targets

- The general Glaze UI actionable floor remains 48px in the reference implementation.
- Perspective or other presentation effects must not reduce the **rendered** interactive region below that floor.
- Wearable actions should expose concise labels or accessible names and remain usable without decorative motion or transparency.
- Destructive meaning must not depend on color alone.

### Lists and rotational navigation

- Vertically ordered lists are the default compact wearable flow.
- Exactly one rotational-navigation item should be current/focusable at a time when roving focus is used.
- Rotary/crown-style input is an enhancement; consumer platforms must preserve an equivalent task path through touch or another native input unless the platform itself defines otherwise.
- Focus/selection must remain visible for non-touch input.

### Status, progress, selection, and glance surfaces

- Keep status and progress surfaces focused on one dominant value or task.
- Use native progress, switch, picker, radio, checkbox, complication, tile, widget, and always-on semantics where the target platform supplies them.
- Host-managed glance surfaces are constrained presentations, not miniature copies of an application.
- Stale or delayed data must not be presented as current.
- Sensitive state must respect platform privacy/redaction behavior.

### Materials and motion

Current 2.0 material terminology is Canvas / Surface / Soft Glaze / Glaze / Deep Glaze / Live Glaze. Older wearable references to Solid/Raised/Functional Glass/Clear Glass describe historical 1.x semantics and are not current 2.0 material names.

Wearable motion remains brief and task-subordinate. Reduced-motion mode must remove nonessential transformation while preserving selection, focus, and task completion. Reduced-transparency or unsupported advanced effects must resolve to readable, bounded surfaces.

## Historical precursor mapping

The repository retains older 1.x Wearable Development Candidate component/native artifacts for audit and migration research. They are not deleted because they contain useful platform-native experiments, but they are **historical evidence only** and cannot satisfy a Glaze UI 2.0 conformance or native-device claim without explicit 2.0 migration and revalidation.

## Native consumer acceptance

A downstream wearable application must separately validate the platform-specific behavior it ships: round/rectangular safe areas as applicable, touch-only completion, rotary/crown mapping, large text, screen-reader semantics, reduced motion/transparency, native back/dismiss behavior, interruption/restoration, system-hosted surfaces, performance, packaging, and representative real-device operation.
