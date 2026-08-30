# Visual Excellence — Glaze UI 2.1 Candidate

Status: **Candidate**

Visual Excellence is a release-quality dimension, not a decorative preference. It evaluates whether a technically conformant interface is also intentional, coherent, refined, accessible, and recognizably Glaze UI.

## 1. Gate model

Visual Excellence uses two complementary evidence classes:

- **Objective conformance** — measurable rules such as token usage, target size, contrast, state presence, geometry bounds, accessibility mappings, supported form factors, and fallback definitions. Objective violations may fail automated validation.
- **Human visual review** — perceptual judgments such as optical balance, composition, rhythm, typography craft, material restraint, icon quality, motion quality, hierarchy, polish, and product personality. Human-review findings must be recorded as review evidence rather than disguised as deterministic numeric failures.

A major component or GoreeCloud application release may be blocked when human review finds material visual-quality defects even if automated checks pass.

## 2. Required review dimensions

Reviewers evaluate, as applicable:

1. Composition and attention hierarchy.
2. Proportion, alignment, optical balance, and concentric geometry.
3. Spacing, rhythm, whitespace, and density.
4. Typography hierarchy, line length, baselines, truncation, and reflow.
5. Color harmony, semantic correctness, contrast, and ambient restraint.
6. Surface hierarchy, Glaze Material selection, and Material Budget discipline.
7. Icon identity, optical weight, small-size clarity, and badge/focus clearance.
8. Component state completeness and quality.
9. Connected Transformation continuity, motion purpose, settling, interruption, and reversal.
10. Reachability, target comfort, pointer/keyboard precision, and native interaction quality.
11. Responsive/form-factor transformation and task continuity.
12. Light, Dark, and Deep Dark quality where supported.
13. Reduced Motion, Reduced Transparency, Increased Contrast, Large Text, Forced Colors, Touch Assistance, and Solid material quality where supported.
14. Full/Balanced/Constrained/Minimal performance-profile quality where supported.
15. Loading, empty, offline, error, conflict, restricted, protected, syncing, and recovery states.
16. Distinct product personality within the shared Glaze grammar.
17. Overall finish: the interface should not contain visibly temporary, generic, inconsistent, careless, or framework-default presentation that weakens the intended experience.

## 3. Optical correctness

Mathematical equality is not automatically perceptual equality. Governed optical correction is allowed for icon alignment, glyph centering, baseline relationships, padding, surface tint/opacity, corner transitions, and comparable visual balancing when:

- the semantic geometry and accessible target remain correct;
- the correction is small and purposeful rather than arbitrary;
- repeated components use a consistent rule or documented exception;
- the result is checked in relevant appearance, density, and accessibility modes; and
- the correction does not conceal an underlying layout defect.

## 4. Restraint rules

Review should flag excessive high-intensity material, blur, transparency, motion, gradients, rounding, shadow, decorative shapes, ambient color, or unrelated animation. The governing question is whether each visual treatment improves hierarchy, relationship, meaning, ergonomics, or atmosphere without competing with content.

Content-heavy workspaces should normally devote most area to Canvas/Surface. Glaze, Deep Glaze, and Live Glaze should remain interaction/state tools rather than background decoration.

## 5. State completeness

Visual acceptance samples must include applicable primary and secondary states, not only the default happy path. At minimum, reviewers should consider default, hover/focus where relevant, pressed, selected, disabled, loading, empty, error, offline/degraded, and any domain-critical privacy/security/backup/sync/identity states.

No state is exempt from visual craft because it is uncommon.

## 6. Accessibility-mode beauty

Accessibility adaptations are first-class renderings. A review fails when an accessibility mode is functionally correct but visibly appears broken, unfinished, unbalanced, or abandoned compared with the ordinary presentation.

Reduced Transparency should use intentional opaque/tonal hierarchy. Increased Contrast should strengthen distinction without indiscriminate darkening. Reduced Motion should preserve understandable state relationships without unnecessary travel. Large Text should recompose rather than squeeze. Forced Colors should preserve native/system semantics and unmistakable focus/state boundaries.

## 7. Performance fallback beauty

Fallbacks must look designed rather than damaged. Advanced graphics may disappear, but typography, composition, spacing, geometry, state communication, and semantic color must remain strong. Simplification is acceptable; loss of hierarchy is not.

## 8. Evidence record

A visual-review record should identify:

- exact source revision;
- release/Candidate version;
- reviewed flows/components;
- platform/form factor and viewport/device class;
- appearance, density, accessibility, and performance profile;
- reviewer/date;
- blocking findings;
- non-blocking recommendations;
- accepted optical corrections;
- screenshots or rendered evidence locations where permitted; and
- final disposition: Accepted, Accepted with follow-up, Rework required, or Incomplete evidence.

A prior review is not evidence for a later changed revision unless the changed scope is proven irrelevant to the reviewed presentation.

## 9. Signature test

The finished experience should communicate Glaze UI through the whole system: calm content areas, selective Glaze interaction islands, ergonomic placement, disciplined geometry and color, strong typography, purposeful depth/motion, connected state changes, adaptive form-factor behavior, accessibility quality, product individuality, and exceptional polish.

Blur + transparency + rounded corners + springs is not a valid substitute for the signature test.

## 10. Candidate boundary

This document establishes the 2.1 Candidate review contract. It does not by itself prove any application visually accepted, and it does not change the current Stable target from 2.0.0. Stable promotion requires representative rendered evidence and recorded human visual review against the exact promotion revision.
