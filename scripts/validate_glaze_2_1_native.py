#!/usr/bin/env python3
"""Fail-closed structural validation for Glaze UI 2.1 native/consumer Candidate work."""
from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []


def fail(message: str) -> None:
    ERRORS.append(message)


def text(path: str) -> str:
    target = ROOT / path
    if not target.is_file():
        fail(f"missing required file: {path}")
        return ""
    return target.read_text(encoding="utf-8")


def data(path: str) -> dict:
    raw = text(path)
    if not raw:
        return {}
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {path}: {exc}")
        return {}
    if not isinstance(value, dict):
        fail(f"{path} top level must be an object")
        return {}
    return value


def main() -> int:
    if text("VERSION").strip() != "2.0.0":
        fail("Glaze UI 2.1 native Candidate work must keep VERSION at 2.0.0")

    app_gradle = text("reference/native/android/buildable/app/build.gradle.kts")
    root_gradle = text("reference/native/android/buildable/build.gradle.kts")
    manifest = text("reference/native/android/buildable/app/src/main/AndroidManifest.xml")
    activity = text("reference/native/android/buildable/app/src/main/java/com/goreecloud/glazeui/reference/android/MainActivity.java")
    native_readme = text("reference/native/android/README.md")
    runtime = text("scripts/validate_glaze_2_1_android_runtime.py")
    workflow = text(".github/workflows/glaze-2.1-android-native.yml")
    lifecycle = data("registry/lifecycle.json")
    consumers = data("consumers/registry.json")
    schema = data("schemas/consumer-registry.schema.json")
    migration = text("MIGRATION_2_0_TO_2_1.md")
    adoption = text("ADOPTION.md")
    stability = text("STABILITY.md")
    files_reference = text("reference/candidate-2.1-files.html")

    for marker in ("compileSdk = 36", "targetSdk = 36", "minSdk = 28", "JavaVersion.VERSION_17"):
        if marker not in app_gradle:
            fail(f"Android app Gradle contract missing: {marker}")
    if 'id("com.android.application") version "9.3.0"' not in root_gradle:
        fail("Android reference must pin AGP 9.3.0")
    if "android.permission.INTERNET" in manifest or "WebView" in activity:
        fail("Android reference must remain native and network-independent rather than a WebView")
    for marker in (
        "MIN_TOUCH_DP = 48",
        "TOUCH_ASSISTANCE_DP = 56",
        "Content is solid. Interaction is glazed.",
        "Canvas: true black",
        "Reduced Transparency: Solid interaction treatment",
        "no live GoreeCloud state",
        "setClipToPadding(true)",
        "setOnApplyWindowInsetsListener",
        "getSystemWindowInsetTop()",
        "setStateListAnimator(null)",
        "setElevation(0f)",
    ):
        if marker not in activity:
            fail(f"Android native reference missing: {marker}")
    if "physical-device acceptance" not in native_readme:
        fail("Android native README must preserve physical-device evidence boundary")
    if "system-bar insets" not in native_readme or "200%" not in native_readme:
        fail("Android native README must document system-bar inset and 200% text evidence")

    for marker in (
        "android-light-balanced.png",
        "android-deep-dark-solid.png",
        "android-large-text-touch-assistance.png",
        '"physicalDevice": False',
        "uiautomator",
        "exact_source_revision",
        '"git", "-C", str(ROOT), "rev-parse", "HEAD"',
        "sourceRevision",
    ):
        if marker not in runtime:
            fail(f"Android runtime validator missing: {marker}")

    for marker in (
        "Check out exact source revision",
        "Build Glaze UI 2.1 Android handheld reference APK",
        "Create deterministic Android handheld emulator",
        "Run Glaze UI 2.1 Android emulator acceptance",
        "Upload Android native Candidate evidence",
        "scripts/validate_glaze_2_1_native.py",
        "scripts/validate_glaze_2_1_android_runtime.py",
        "hw.device.name=glaze_android_handheld",
        "if: ${{ success() }}",
    ):
        if marker not in workflow:
            fail(f"Android native workflow missing: {marker}")
    if "create avd --force" in workflow:
        fail("Android native workflow must not rely on interactive avdmanager AVD creation")

    capabilities = lifecycle.get("capabilities", {})
    android_ref = capabilities.get("android-native-reference-2.1", {})
    if android_ref.get("status") != "candidate":
        fail("android-native-reference-2.1 must be Candidate")
    if android_ref.get("implementation") != "reference/native/android/buildable":
        fail("android-native-reference-2.1 implementation path")
    android_acceptance = capabilities.get("android-handheld-emulator-acceptance-2.1", {})
    if android_acceptance.get("status") != "candidate":
        fail("android-handheld-emulator-acceptance-2.1 must be Candidate")
    if android_acceptance.get("runtimeValidator") != "scripts/validate_glaze_2_1_android_runtime.py":
        fail("Android emulator acceptance runtime validator path")
    if android_acceptance.get("physicalDeviceAccepted") is not False:
        fail("Android emulator acceptance must explicitly keep physicalDeviceAccepted false")

    consumer_cap = capabilities.get("consumer-conformance-registry-2.1", {})
    if consumer_cap.get("status") != "candidate":
        fail("consumer-conformance-registry-2.1 must be Candidate")
    if consumer_cap.get("implementation") != "consumers/registry.json":
        fail("2.1 consumer registry must extend canonical consumers/registry.json")
    if consumer_cap.get("validator") != "scripts/validate_consumer_registry.py":
        fail("2.1 consumer registry validator path")

    assessment = consumers.get("candidateAssessment", {})
    if assessment.get("version") != lifecycle.get("activeCandidate"):
        fail("consumer Candidate assessment must target lifecycle activeCandidate")
    if assessment.get("lifecycle") != "candidate":
        fail("consumer Candidate assessment lifecycle")
    if assessment.get("consumerEligible") is not False or assessment.get("productionEligible") is not False:
        fail("2.1 Candidate assessment must never become consumer/production eligible")
    if not isinstance(assessment.get("evaluations"), list):
        fail("2.1 Candidate evaluations must be a list")
    if assessment.get("evaluations"):
        fail("this tranche must not invent downstream 2.1 consumer evaluations")

    if schema.get("$id") != "https://goreecloud.dev/schemas/glaze-ui/consumer-registry.schema.json":
        fail("consumer registry schema id")
    required = set(schema.get("required", [])) if isinstance(schema.get("required"), list) else set()
    if not {"schemaVersion", "stableBaseline", "requiredConsumerVersion", "candidateAssessment", "consumers"}.issubset(required):
        fail("consumer registry schema must require Stable and Candidate audit fields")

    rules = lifecycle.get("promotionRules", {})
    if rules.get("candidateMaySatisfyStableConsumerConformance") is not False:
        fail("Candidate must not satisfy Stable consumer conformance")
    if rules.get("stableVersionFileMustRemain") != "2.0.0":
        fail("Stable VERSION boundary must remain 2.0.0")
    if capabilities.get("glaze-motion", {}).get("status") != "experimental":
        fail("Glaze Motion must remain Experimental")

    migration_lower = migration.lower()
    for marker in (
        "current stable: **2.0.0**",
        "target after formal promotion: **2.1.0**",
        "glaze motion remains experimental",
        "does not promote applications by declaration",
        "visual excellence",
        "rollback",
        "central consumer-registry effect",
    ):
        if marker not in migration_lower:
            fail(f"2.0 to 2.1 migration guide missing: {marker}")
    if "MIGRATION_2_0_TO_2_1.md" not in adoption:
        fail("ADOPTION.md must link the 2.0 to 2.1 migration guide")
    if "MIGRATION_2_0_TO_2_1.md" not in stability:
        fail("STABILITY.md must link the 2.0 to 2.1 migration guide")
    if "2.1 remains Candidate" not in adoption:
        fail("ADOPTION.md must preserve 2.1 Candidate boundary")
    if "human Visual Excellence" not in stability:
        fail("STABILITY.md must preserve human Visual Excellence promotion boundary")

    if "＋ New" in files_reference:
        fail("Files reference must not use unsupported full-width plus glyph")
    if '<span aria-hidden="true">+</span> New' not in files_reference:
        fail("Files reference must expose the deterministic New-action plus treatment")

    if ERRORS:
        print("Glaze UI 2.1 native/consumer Candidate validation FAILED:", file=sys.stderr)
        for item in ERRORS:
            print(f"  - {item}", file=sys.stderr)
        return 1
    print("Glaze UI 2.1 native Android, migration and consumer-assessment structure validated.")
    print("Current Stable remains 2.0.0; no downstream 2.1 conformance is implied.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
