# Glaze UI Stability Contract

Glaze UI is a shared production dependency for GoreeCloud applications. Stability therefore means more than a passing build: the design system must provide a predictable semantic contract, repeatable validation, controlled change management, documented compatibility, and representative rendered evidence.

## Current release boundary

- **Stable baseline:** Glaze UI 1.3.0 on `main`.
- **Candidate line:** Glaze UI 1.4.0 remains isolated in its form-factor candidate branch and pull request until all required promotion evidence is complete.
- Stable consumers are never migrated automatically when a newer candidate exists.
- Experimental roadmap concepts do not alter the Stable contract unless they enter a separately versioned, reviewed, validated release line.

## Stability principles

1. **Stable means compatible.** Patch changes must not silently alter established semantic roles, required component behavior, token meaning, or supported interaction contracts.
2. **Stable means fail closed.** Required files, semantic roles, accessibility fallbacks, acceptance rules, or release-boundary declarations may not disappear without validation failing.
3. **Stable means evidence-bound.** Promotion decisions must identify the exact candidate SHA and the exact validation evidence used.
4. **Stable means product-safe.** A design-system change does not imply downstream application readiness. Each consumer retains application-specific adoption and acceptance responsibility.
5. **Stable means accessible under degradation.** Reduced motion, reduced transparency where supported, increased contrast, forced colors, missing backdrop filtering, and other documented resilience states remain usable.
6. **Stable means local and privacy-conscious.** Canonical presentation must not acquire unnecessary remote fonts, icons, scripts, analytics, trackers, or runtime dependencies.
7. **Stable means reversible.** Every promotion or material contract change must have an explicit Git rollback path and must not require unrelated infrastructure rollback.

## Change classification

### Patch release

A patch release may include compatible corrections such as:

- bug fixes;
- accessibility or resilience fixes;
- validation hardening;
- documentation clarification;
- compatible visual polish that does not redefine semantic meaning;
- deterministic test-harness reliability corrections that do not weaken assertions.

A patch release must not repurpose an existing token, remove a required semantic role, or require consumers to redesign previously conformant behavior.

### Minor release

A minor release may add compatible tokens, primitives, components, acceptance cases, or platform semantics. Existing Stable semantics must remain valid unless an explicit migration is documented and the change is judged non-breaking.

New minor versions remain Candidate until the full promotion gate passes.

### Major release

A major release is required when the design system intentionally changes established semantic meaning, removes a supported contract, introduces incompatible component behavior, or requires consumers to perform a breaking migration.

## Stable promotion gate

A candidate may be promoted to Stable only when all applicable conditions below are satisfied:

1. Repository validation passes on the exact final candidate SHA.
2. Rendered reference acceptance passes on the exact final candidate SHA.
3. Required light/dark, accessibility, resilience, and supported form-factor cases pass.
4. No required acceptance case is silently skipped; unsupported cases are explicitly recorded.
5. Defects found during acceptance are corrected without weakening the affected gate.
6. The final candidate has a documented compatibility and migration assessment.
7. The component-status record is accurate for the candidate.
8. Stable documentation, version metadata, changelog, and release status agree.
9. Any platform-native or real-device evidence required by the candidate's scope is completed before promotion.
10. The pull request is promoted from draft only after the complete exact-head gate is green.
11. Merge uses expected-head protection so a changed candidate cannot be promoted using stale evidence.
12. The resulting Stable commit and rollback point are recorded.

If any applicable gate is incomplete, the release remains Candidate.

## Stable maintenance rules

While 1.3.x is the Stable line:

- compatibility and correctness outrank feature expansion;
- no speculative intelligence, ambient-computing, operating-experience, or other roadmap concept is added to the Stable contract merely because it has been discussed;
- new candidate work must remain isolated from `main` until promotion;
- consumer applications may continue targeting 1.3.0 while a newer candidate is evaluated;
- documentation-only clarifications may merge when they preserve the existing Stable semantics and pass the normal exact-head gate.

## Regression blockers

The following block Stable promotion or a Stable patch merge when applicable:

- missing or renamed required semantic tokens without migration;
- loss of keyboard focus visibility;
- actionable targets below the documented minimum where the platform permits compliant sizing;
- loss of persistent field labels or programmatic field feedback relationships;
- reduced-motion behavior that retains nonessential spatial transformation;
- unreadable glass surfaces when transparency or backdrop filtering is unavailable;
- forced-colors loss of focus, selection, checked, progress, or destructive distinction;
- new unapproved remote presentation dependencies;
- generic scaled form-factor layouts where purpose-built composition is required;
- version, token metadata, documentation, and release-status disagreement;
- acceptance evidence that is not bound to the final candidate SHA.

## Consumer compatibility

A GoreeCloud application may remain on an older Stable Glaze UI release while a newer Stable release exists when migration would introduce unnecessary risk. Consumer upgrades should be controlled, version-specific, and validated against the application's actual surfaces rather than achieved by copying the reference stylesheet wholesale.

Platform-native controls remain preferred where they provide stronger native accessibility or interaction behavior. Glaze conformance is semantic, not a requirement to reproduce web implementation details on every platform.

## Stability review cadence

Before a Stable release or material Stable contract change, review:

- version and token metadata;
- required files and validator coverage;
- component lifecycle classifications;
- conformance and acceptance contracts;
- representative rendered evidence;
- accessibility and resilience behavior;
- privacy/runtime-dependency boundaries;
- downstream migration impact;
- rollback instructions;
- unresolved defects or candidate-only assumptions.

The goal is a design system that GoreeCloud applications can depend on without continuous visual churn or surprise semantic changes.
