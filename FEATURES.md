# GLAZE UI V1.5 — Features

## Status convention

This file describes capabilities present in the current Stable GLAZE UI V1.5 source tree at machine version `1.5.1` or required by its active Stable contracts. V1.5.1 is the Stable qualification-hardening patch for the V1.5 Context + Capability Awareness line. Downstream adoption, release publication, deployment, and application production acceptance remain separate evidence-bound transitions.

## Design-system capabilities

- Foundation tokens for color, spacing, radii, typography, focus, targets, elevation, motion, semantic state, and responsive composition.
- Reusable components with adaptive, runtime-aware, accessibility-aware, and form-factor-aware behavior.
- Responsive structure and layout contracts across supported form factors.
- Layered materials, overlays, panels, and accessibility-aware transparency behavior.
- Interaction states for focus, hover, press, selection, disabled behavior, input adaptation, and continuity.
- Motion primitives with reduced-motion handling and native-motion mappings.
- Accessibility contracts for contrast, focus visibility, target sizing, text scaling, forced colors, reduced transparency, semantic announcements, keyboard behavior, and assistive-technology continuity.
- Semantic color architecture and adaptive color validation.
- Iconography, icon-construction, and product-identity contracts.
- Workspace navigation, System Shell semantics, Universal Search, capsule, smart-rail, morph-card, Aurora surface, and intelligence-oriented interaction patterns inherited through the Stable V1 line.
- V1.4.1 Optical Intelligence capabilities, including protected semantic surfaces, capability-aware optical degradation, content-aware frost, semantic blur protection, environment tinting, chromatic depth layers, environmental color memory, and visual-regression authority.
- Governed Context + Capability Resolution that combines authoritative context, capability state, application intent, accessibility needs, runtime conditions, connectivity, input, and window state into presentation decisions without becoming an authorization or execution authority.
- Provider authority/domain ownership with provenance and fail-closed handling of conflicting or unknown ownership.
- Contextual composition and presentation-density adaptation with accessibility precedence.
- Runtime-pressure, connectivity, window-state, posture, and constrained-environment continuity without rewriting capability truth.
- Capability-aware navigation and controls with stable primary-action ordering.
- Predictable contextual adaptation of non-primary actions.
- Explicit unavailable/degraded explanations and recovery metadata.
- User-initiated fallback suggestions and graceful degradation without automatic fallback execution, automatic permission requests, consequential execution, or automatic navigation.
- Privacy-safe explainable diagnostics that omit raw sensitive context and provider identity by default.
- Evidence-presentation and GoreeCloud Mesh evidence-profile contracts.
- Native reference material for supported Android, Wear OS, watchOS, foldable/posture, and other governed platform surfaces where repository evidence exists.
- Consumer registry and conformance-evidence validation for downstream GoreeCloud applications.

## Stable qualification capabilities

The current Stable V1.5.1 qualification is the governing shared qualification.

It retains the sixteen accepted V1.5.0 obligations and adds two independently reviewed qualification expansions, for eighteen accepted shared obligations in total:

- `performance-representative-budget` — accepted for the reviewed representative Zorin OS 17.3 / Firefox 156.0 / Lenovo IdeaPad 3 15IIL05 environment.
- `platform-posture-continuity` — accepted for the approved Pixel Fold Android Emulator target runtime under `GCU-ADR-GLAZE-V151-POSTURE-TR-001`.

These shared qualification claims are bounded to their reviewed environments. They do not automatically establish downstream application performance, physical-device, posture, deployment, or production acceptance.

## Stable validation and authority

The repository includes fail-closed validation for the current V1.5.1 Stable authority, qualification scope, source-impact continuity, lifecycle state, consumer registry, accessibility and form-factor requirements, context/capability resolution, privacy and authority boundaries, performance qualification, posture continuity, release state, and related contracts.

Current Stable authority is defined by:

- `VERSION` — `1.5.1`.
- `GLAZE_UI_V1_5.md` — current Stable family contract.
- `contracts/v1.5.1/stable-scope.json` — exact V1.5.1 Stable qualification scope.
- `acceptance/v1.5.1-stable.md` — Stable acceptance record.
- `GLAZE_UI_V1_5_1_HARDENING.md` — completed V1.5.1 qualification-hardening record.
- `registry/lifecycle.json` — lifecycle authority.
- `js/glaze-v1.5.1.mjs` — current Stable runtime entrypoint.
- `css/glaze-v1.4.1.css` — inherited Stable optical/web material baseline.
- `scripts/verify_glaze_v1_5_1_stable.mjs` — fail-closed Stable authority gate.

V1.5.0 remains the immediate known-good Stable rollback baseline.

## Development successor boundary

The repository may contain Development-only successor language, contracts, tokens, validators, or reference inputs. Those artifacts do not change the current V1.5.1 Stable authority, lifecycle, runtime/web entrypoints, downstream consumer acceptance, release publication, deployment, or production status unless they complete a separate governed lifecycle promotion.
