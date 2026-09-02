# Buildable Android Glaze UI 2.2 Candidate Reference

This is the bounded native Android handheld reference for Glaze UI `2.2.0-candidate.1`.

It exists to prove that claimed 2.2 System Shell interaction semantics can be implemented with Android framework primitives on a hosted emulator. It does **not** make Glaze UI 2.2 Stable and does not certify downstream GoreeCloud applications, physical devices, OEM behavior, TalkBack, Switch Access, signing, distribution, battery behavior, or human Visual Excellence.

Toolchain contract:

- Android Gradle Plugin: 9.3.0
- compileSdk / targetSdk: 36
- minSdk: 28
- Java: 17
- CI Gradle distribution: verified 9.5.0
- application ID: `com.goreecloud.glazeui.reference.android22`

The reference uses Android framework UI primitives only; it does not use WebView.

Test-only Intent extras:

- `appearance`: `light`, `dark`, or `deep-dark`
- `reducedTransparency`: boolean
- `touchAssistance`: boolean

The reference validates the bounded native mapping for:

- explicit Candidate / Stable lifecycle identity;
- 48 dp standard and 56 dp Touch Assistance targets;
- Universal Search focus and deterministic source-first results;
- destructive search confirmation before execution;
- generated-answer source provenance;
- Control Center toggle/range semantics;
- Search and Control Center mutual exclusivity; and
- Reduced Transparency as an effects-free solid treatment.
