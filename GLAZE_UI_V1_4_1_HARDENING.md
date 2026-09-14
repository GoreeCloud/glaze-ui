# GLAZE UI V1.4.1 — Human Validation & Optical Hardening

**Lifecycle:** Planned follow-up  
**Baseline:** GLAZE UI V1.4 / `1.4.0` Stable  
**Purpose:** Human validation, human verification, physical-device qualification, and subjective optical polish.

V1.4.1 is the explicit home for human-dependent validation deferred from the V1.4.0 Stable release by owner direction. Deferral does not mean these checks passed; it means they are non-blocking for V1.4.0 lifecycle activation and remain open work for this patch track.

## Required human-validation work

- Review Content-Aware Frost over calm, noisy, bright, dark, photographic, video, and high-motion backgrounds.
- Review Semantic Blur Protection around text, icons, faces, labels, controls, and critical status regions.
- Review environment tint and light warmth across light, dark, deep-dark, dawn, day, dusk, and night contexts.
- Review chromatic depth separation for base, raised, overlay, and modal surfaces.
- Review environmental color memory for subtlety, identity preservation, and unwanted color contamination.
- Validate Reduced Transparency, Increased Contrast, Forced Colors, Reduced Motion, large text, RTL, keyboard, touch, pointer, switch, voice, and supported assistive technologies where applicable.
- Validate supported Android/OEM, Linux compositor/window, desktop, mobile, tablet, TV, watch, foldable, and other claimed form-factor behavior on representative physical devices.
- Measure representative real-device performance, thermal/power behavior, animation smoothness, and degradation behavior.
- Perform subjective polish review for glass quality, depth, warmth, animation/touch feel, visual balance, and GoreeCloud identity recognition.

## Evidence rule

Every completed item must identify the tested build/revision, device or environment, reviewer, scope, result, and any accepted limitation. Automated evidence may support a review but must not be relabeled as human evidence.

V1.4.1 uses a structured multi-session evidence protocol so one record can combine review sessions across Android, Linux, desktop, mobile, tablet, TV, watch, foldable, accessibility, and performance environments without flattening them into one misleading global pass state.

The protocol authority is:

- `contracts/v1.4.1/human-validation.contract.json` — canonical required-check matrix and fail-closed rules.
- `schemas/v1.4.1-human-validation-record.schema.json` — Draft 2020-12 structural schema for editor/tool validation; schema validity alone is never human acceptance.
- `acceptance/v1.4.1-human-validation.template.json` — deliberately pending template; never acceptance evidence by itself.
- `scripts/verify_glaze_v1_4_1_human_validation_schema.mjs` — contract/schema/template parity verifier.
- `scripts/verify_glaze_v1_4_1_human_validation.mjs` — machine validation of evidence authority, coverage, revision binding, and promotion eligibility.

Each human review session must identify the exact tested source revision, build/artifact identity, timestamp with timezone, named reviewer and role, platform, OS version, device/environment, form factor, display context, relevant input modalities, assistive technologies, findings, limitations, and evidence references.

A check may be marked `not_applicable` only with an explicit rationale. `pending`, `blocked`, or `fail` cannot satisfy promotion. A claimed `pass` or `fail` requires at least one evidence reference. Machine-generated supporting artifacts can be referenced, but the record itself must remain human-authorized.

### Verification

Validate the schema/contract parity, protocol, and synthetic negative tests without claiming human acceptance:

```sh
node scripts/verify_glaze_v1_4_1_human_validation_schema.mjs
node scripts/verify_glaze_v1_4_1_human_validation.mjs --source-only
node scripts/verify_glaze_v1_4_1_human_validation.mjs --self-test
```

Validate a real record without asserting patch promotion:

```sh
node scripts/verify_glaze_v1_4_1_human_validation.mjs --record path/to/human-record.json
```

Run the fail-closed promotion gate only when a real record exists and the exact reviewed implementation revision is known:

```sh
node scripts/verify_glaze_v1_4_1_human_validation.mjs \
  --record path/to/human-record.json \
  --promotion \
  --expected-revision <40-character-reviewed-revision>
```

The schema validator and verifier's synthetic self-test are protocol testing only. They are never human evidence, never physical-device evidence, and never V1.4.1 acceptance.

## Patch acceptance

V1.4.1 may be promoted only after its claimed human/manual/physical-device evidence is actually recorded and any release-blocking findings are resolved or explicitly scoped out of the supported claim. V1.4.1 must not retroactively rewrite V1.4.0 evidence.

Promotion additionally requires the structured record to cover every canonical required check, contain no unresolved exceptions, contain no `pending`, `blocked`, or `fail` results, explicitly declare an accepted decision, explicitly declare promotion eligibility, and bind every contributing review session to the exact revision supplied to the promotion gate.
