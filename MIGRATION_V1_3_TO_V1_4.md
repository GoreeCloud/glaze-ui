# Migrating GLAZE UI V1.3 to V1.4

GLAZE UI V1.4 is an additive upgrade over V1.3. Existing V1.3 token and component contracts remain valid; consumers should change their Stable entrypoints and then opt into optical context where appropriate.

## Required migration

1. Replace the web entrypoint with `css/glaze-v1.4.0.css`.
2. Replace the runtime entrypoint with `js/glaze-v1.4.0.mjs`.
3. Update repository-local Glaze UI version assertions to `1.4.0`.
4. Re-run consumer-local accessibility, workflow, rollback, and production acceptance checks for the surfaces actually shipped.

## Optional optical integration

Consumers may use `resolveGlazeOptics`, `applyGlazeOptics`, or `createGlazeOpticalEngine` from the v1.4 runtime. Context signals are optional and must be supplied by the consumer through locally approved adapters.

Do not collect new telemetry, camera data, browsing content, personal data, or remote context merely to drive Glaze optics. Glaze UI grants no collection authority. Any contextual source remains subject to the consumer's Wardveil Security and Privacy Shield requirements.

## Accessibility requirements

Consumer adapters must propagate relevant accessibility state. Forced Colors and Reduced Transparency must result in the solid accessible path. Increased Contrast must retain the v1.4 stronger-protection behavior. Do not override these outcomes with product-local visual effects.

## Rollback

V1.3.0 remains the immediate known-good rollback baseline. A rollback changes the CSS/runtime entrypoints back to `glaze-v1.3.0` and must be verified against the consumer's repository-local release process.

## Human validation

Human optical validation and human verification are tracked in V1.4.1 and do not block the shared V1.4.0 Stable lifecycle. Consumer applications may still impose stricter local release requirements; this shared deferral does not override product-specific safety, accessibility, or regulatory obligations.
