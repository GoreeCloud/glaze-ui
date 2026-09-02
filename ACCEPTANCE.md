# Glaze UI Release Acceptance Protocol

Stable promotion requires exact-revision source validation plus representative rendered/accessibility acceptance. `STABILITY.md` governs compatibility/promotion; `COMPONENT_STATUS.md` governs lifecycle. Version-specific evidence lives under `acceptance/`.

## Required evidence

Record exact Candidate/promotion SHA, CI run, rendering environment, proposed/final lifecycle status, compatibility/migration impact, lifecycle changes, unresolved/unsupported cases, human Visual Excellence decision where required, native/device evidence where claimed, and rollback boundary. A prior or partial run cannot substitute for the exact final revision.

Merge, release/tag creation, deployment, and downstream consumer acceptance are separate events and must retain exact-revision traceability.

## Representative form-factor matrix

| Profile | Required reference |
| --- | --- |
| Phone / Mobile | 390 × 844 |
| Tablet | 820 × 1180 |
| Desktop | 1280 × 900 |
| Wide Desktop | 1600 × 1000 |
| TV | 1920 × 1080 |

The retained design-system suite also includes representative foldable/hinge-aware, compact wearable and spatial surfaces. Appearance: Light/Dark where applicable plus Deep Dark representative cases. Input: touch/pointer/keyboard/directional/rotational semantics as applicable. Motion: normal and Reduced Motion. Transparency: normal and Reduced Transparency. Contrast: normal/Increased Contrast plus `forced-colors: active` or equivalent. Near-view profiles retain 200% browser zoom/reflow coverage.

Each supported form factor requires a **representative task flow**, not merely a static screenshot. Unsupported or consumer-native cases must be recorded explicitly rather than silently treated as accepted.

## Glaze UI 2.2 core acceptance checks

- no unintended horizontal overflow;
- Workspace → Application → System Overlay → System Panel → Critical System hierarchy remains explicit;
- durable readable content remains solid while transient interaction uses bounded Glaze;
- ordinary composition preserves at most one dominant Glaze panel plus one to three small floating Glaze controls;
- nested backdrop blur remains prohibited;
- Light/Dark/Deep Dark remain legible and hierarchically distinct;
- touch-oriented shell/control targets preserve at least 48 px/dp where governed by 2.2;
- Touch Assistance/far-view contexts preserve at least 56 px/dp where applicable;
- visible focus and non-color state meaning remain intact;
- persistent labels, textarea behavior, checkbox/radio choices, switches, sliders, segmented controls/tabs and progress indicators remain accessible;
- Universal Search preserves immediate query focus, deterministic results before generated interpretation, keyboard traversal, destructive confirmation, Escape semantics and focus restoration;
- Control Center preserves programmatic toggle/range state, dominant-panel exclusivity and focus restoration;
- Intelligence components preserve explicit generated/AI identity and provenance when available without inventing execution or evidence authority;
- Connected Transformation preserves destination/state when spatial/native transition support is unavailable;
- Reduced Motion and Reduced Transparency preserve capability with simplified presentation;
- Increased Contrast and Forced Colors preserve distinctions and focus;
- 200% text and RTL/localization expansion preserve content, action reachability and reading/focus order;
- no unapproved remote presentation dependencies;
- purpose-built Phone/Mobile, Tablet, Desktop, TV, foldable, wearable and spatial behavior is used rather than scaled shells where those contexts are supported;
- performance fallbacks simplify effects before semantics or target geometry;
- advanced optical effects are never required for basic usability.

## Form-factor fidelity acceptance

### Phone / Mobile
Touch/reachability-first; safe-area-aware; reachable frequent actions; intentional transient overlays/sheets; never a shrunken Tablet/Desktop interface.

### Tablet
Intentional rails/panes/split/master-detail where useful; touch remains primary; posture/orientation/window changes preserve state; never a stretched Mobile interface.

### Desktop
Pointer/keyboard workflows, resizable windows, appropriate density, menus/toolbars/shortcuts/context behavior where useful; never an enlarged Mobile interface.

### TV
Far-view legibility; landscape-first; overscan-safe essential content; larger type/targets/spacing; directional focus plus Select/Back-equivalent task flow; no pointer/swipe dependency; focus remains distinct from selection; no unreachable controls or focus traps; Reduced Motion/Forced Colors preserve a strong static focus indicator.

### Foldable
Representative book posture reserves a physical hinge exclusion region; panes remain outside the hinge, preserve minimum usable widths and maintain state/focus/read order through posture changes.

### Wearable
Compact glance-first hierarchy preserves effective targets, native-equivalent completion and rotational/crown navigation when applicable. Design-system compatibility evidence is not native-device certification.

### Spatial
Anchored/floating surfaces preserve semantic focusability and effective target floors at supported depth; a fully flattened no-depth mode remains equivalent and usable. Hardware-specific spatial products require native/real-device acceptance.

## Retained historical regression acceptance

Glaze UI 1.x, 2.0.0 and 2.1.0 source, rendered, interaction, resilience, visual-regression and bounded native evidence remain permanent regression authorities for semantics still required by 2.2. Supersession changes their lifecycle role from current target to historical regression; it does not justify deleting or bypassing those gates.

The 2.1 approved visual baseline remains pinned to `5b46903c18660ae78e7f1aaea39a93136efacda7`. The 2.1 bounded Android handheld runtime remains separately exercised as historical regression evidence.

Glaze Motion remains separately Experimental.

## Glaze UI 2.2 Stable promotion acceptance

For Glaze UI 2.2.0 Stable, the exact final promotion revision must satisfy all applicable gates recorded in `acceptance/2.2-stable.md`, including:

- canonical release/lifecycle state and `VERSION` agreement;
- all 32 component contracts;
- System Shell and component rendered matrices;
- bounded Universal Search and Control Center interaction regression;
- 2.1→2.2 migration compatibility;
- performance and System Glaze-budget evidence;
- Optical Reachability static and rendered acceptance;
- independently rendered source-pinned screenshot regression against immutable human-approved source `0411b0f6dd877aea30e2c5674e1acde0105fd97b`;
- accessibility/input matrices including keyboard, pointer, touch, RTL, 200% text, Reduced Motion, Reduced Transparency, Increased Contrast, Forced Colors and Touch Assistance;
- bounded Android handheld build/emulator/runtime/accessibility/resilience evidence;
- retained historical regression workflows;
- accurate Stable docs, consumer registry and migration boundary; and
- rollback to Glaze UI 2.1.0.

Human Visual Excellence for the 2.2 Optical Reachability presentation was explicitly **Accepted** on 2026-09-01 for the immutable reviewed source above. Exact-head promotion changes must prove presentation continuity rather than silently replacing that human-reviewed source.

## Release closure acceptance

A green promotion PR establishes merge eligibility, not an immutable release by itself. After the exact verified Stable head is merged:

- create immutable `v2.2.0` release/tag anchored to the verified Stable source revision;
- record merge SHA and release/tag target;
- record final required workflow run IDs and artifact digests;
- verify post-merge current-Stable state;
- preserve rollback information; and
- update permanent project documentation/change log without rewriting protected project instructions.

Downstream consumers remain separately migration-gated and production-ineligible until their own exact-revision adoption evidence passes.

## Stability promotion acceptance

Before any Candidate becomes Stable: lifecycle classification is accurate; Experimental/Planned capability is not required; promoted capability has semantics/accessibility/validation/migration guidance; exact final Candidate/promotion revision passes source and rendered/native acceptance applicable to its scope; failed cases are fixed without weakening gates; Stable docs/status/version agree; rollback is identified.

For platform-neutral design-system references, native/real-device execution is not automatically applicable. Native consumers still require product-specific native/real-device acceptance.

**If any required check cannot be executed, the release remains a candidate.**
